# app/services/chat_service.py
from __future__ import annotations
from typing import List, Optional
from app.models import EntradaChat, Documento
from app.services.sheet_service import extract_sheet_id, load_sheet_records

def load_entries_from_document(documento_id: int, sheet_name: str = "respuestas") -> List[EntradaChat]:
    doc = Documento.query.get(documento_id)
    if not doc:
        raise ValueError("Documento no encontrado.")
    sheet_id = extract_sheet_id(doc.enlace)
    if not sheet_id:
        raise ValueError("Enlace de Google Sheet inválido (no se pudo extraer sheet_id).")
    rows = load_sheet_records(sheet_id=sheet_id, sheet_name=sheet_name)
    return [EntradaChat.from_dict(row) for row in rows]

def find_answer(question: str, entries: List[EntradaChat]) -> Optional[str]:
    """
    Matching simple: 'entrada.pregunta' contenida en la pregunta normalizada.
    """
    if not question:
        return None
    q = (question or "").strip().lower()
    for e in entries:
        if not getattr(e, "pregunta", None):
            continue
        if e.pregunta.strip().lower() in q:
            return getattr(e, "respuesta", None)
    return None
