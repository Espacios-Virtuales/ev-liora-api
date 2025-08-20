# app/controllers/membresia_controller.py
from __future__ import annotations
from flask import request
from app.views.responses import success, created, error
from app.services.membresia_service import crear_membresia, obtener_todas_membresias

def registrar_membresia(data: dict):
    if not data or not data.get("nombre"):
        return error("Datos inválidos", code="VALIDATION_ERROR", details={"missing": ["nombre"]}, status=422)
    try:
        m = crear_membresia(nombre=data["nombre"], descripcion=data.get("descripcion"))
        return created({"id": m.id, "nombre": m.nombre})
    except ValueError as ve:
        return error(str(ve), code="VALIDATION_ERROR", status=400)

def obtener_membresias():
    arr = obtener_todas_membresias()
    return success([{"id": m.id, "nombre": m.nombre} for m in arr])
