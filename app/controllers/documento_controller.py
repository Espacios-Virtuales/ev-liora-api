# app/controllers/documento_controller.py
from __future__ import annotations
from app.views.responses import success, created, error
from app.services.documento_service import crear_documento, obtener_todos_documentos

def registrar_documento(data: dict):
    if not data or not data.get("titulo") or not data.get("enlace"):
        return error("Datos inválidos", code="VALIDATION_ERROR", details={"missing": ["titulo", "enlace"]}, status=422)
    try:
        d = crear_documento(data["titulo"], data["enlace"])
        return created({"id": d.id})
    except ValueError as ve:
        return error(str(ve), code="VALIDATION_ERROR", status=400)

def obtener_documentos():
    arr = obtener_todos_documentos()
    return success([{"id": d.id, "titulo": d.titulo} for d in arr])
