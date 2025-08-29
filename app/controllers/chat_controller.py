# app/controllers/chat_controller.py
from __future__ import annotations
from typing import List, Dict
from flask import request
from app.views.responses import success, error
from app.services.chat_service import load_entries_from_document, find_answer
from app.services.drive_csv_service import (
    csv_from_file_id_or_url,
    csv_from_folder_and_name,
)
from app.models import EntradaChat


def _rows_to_entries(rows: List[Dict]) -> List[EntradaChat]:
    """Convierte filas (dicts) en EntradaChat usando la conversión estándar."""
    return [EntradaChat.from_dict(r) for r in rows]


def responder_pregunta(data: dict):
    """
    data (soporta 2 modos):

    A) CSV en Google Drive (RECOMENDADO)
       - Por fileId o URL:
         { "pregunta": str, "file_id_or_url": str, "sep": "," (opcional) }
       - Por carpeta + nombre de archivo:
         { "pregunta": str, "folder_name": str, "filename": str, "sep": "," (opcional) }

    B) (Compat) Google Sheets por documento_id (flujo legado):
         { "pregunta": str, "documento_id": int, "sheet_name": "respuestas" }

    Retorna: { "respuesta": str }
    """
    # Validación mínima de pregunta
    if not data or not data.get("pregunta"):
        return error(
            "Datos inválidos",
            code="VALIDATION_ERROR",
            details={"missing": ["pregunta"]},
            status=422,
        )

    try:
        pregunta = data["pregunta"]
        sep = data.get("sep")

        entries: List[EntradaChat] = []

        # --- Modo CSV: file_id_or_url ---
        if data.get("file_id_or_url"):
            rows = csv_from_file_id_or_url(data["file_id_or_url"], sep=sep)
            entries = _rows_to_entries(rows)

        # --- Modo CSV: folder_name + filename ---
        elif data.get("folder_name") and data.get("filename"):
            rows = csv_from_folder_and_name(
                folder_name=data["folder_name"],
                filename=data["filename"],
                sep=sep,
            )
            entries = _rows_to_entries(rows)

        # --- Modo legado: Google Sheet por documento_id ---
        elif data.get("documento_id"):
            entries = load_entries_from_document(
                data["documento_id"], data.get("sheet_name", "respuestas")
            )
        else:
            # Si no calza ninguna variante de entrada
            return error(
                "Datos insuficientes: especifica 'file_id_or_url' o ('folder_name' y 'filename') o 'documento_id'.",
                code="VALIDATION_ERROR",
                details={"expected": ["file_id_or_url | folder_name+filename | documento_id"]},
                status=422,
            )

        # Resolver respuesta
        ans = find_answer(pregunta, entries) or "No tengo una respuesta aún. ¿Quieres hablar con un humano?"
        return success({"respuesta": ans})

    except FileNotFoundError as fnf:
        # CSV no encontrado (carpeta/archivo)
        return error(str(fnf), code="NOT_FOUND", status=404)

    except TypeError as te:
        # No es CSV compatible (mimetype)
        return error(str(te), code="UNSUPPORTED_MEDIA_TYPE", status=415)

    except ValueError as ve:
        # Validaciones del flujo legado (documento no encontrado / enlace inválido)
        return error(str(ve), code="VALIDATION_ERROR", status=400)

    except Exception as e:
        return error(
            "Error resolviendo la pregunta",
            code="INTERNAL_ERROR",
            details=str(e),
            status=500,
        )
