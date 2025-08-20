# app/controllers/chat_controller.py
from __future__ import annotations
from flask import request
from app.views.responses import success, error
from app.services.chat_service import load_entries_from_document, find_answer

def responder_pregunta(data: dict):
    """
    data = { "documento_id": int, "pregunta": str, "sheet_name": "respuestas" }
    """
    if not data or not data.get("documento_id") or not data.get("pregunta"):
        return error("Datos inválidos", code="VALIDATION_ERROR", details={"missing": ["documento_id", "pregunta"]}, status=422)
    try:
        entries = load_entries_from_document(data["documento_id"], data.get("sheet_name", "respuestas"))
        ans = find_answer(data["pregunta"], entries) or "No tengo una respuesta aún. ¿Quieres hablar con un humano?"
        return success({"respuesta": ans})
    except ValueError as ve:
        return error(str(ve), code="VALIDATION_ERROR", status=400)
    except Exception as e:
        return error("Error resolviendo la pregunta", code="INTERNAL_ERROR", details=str(e), status=500)
