# app/controllers/clientes_controller.py
from __future__ import annotations
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from app.services.cliente_service import crear_cliente
from app.views.responses import created, success, error
from app.views.serializers import cliente_to_dict
from app.models import Cliente

bp = Blueprint("clientes", __name__)

def post_clientes():
    data = request.get_json(silent=True) or {}
    if not data.get("nombre"):
        return error("Datos inválidos", code="VALIDATION_ERROR", details={"missing": ["nombre"]}, status=422)
    try:
        c = crear_cliente(
            nombre=data["nombre"],
            slug=data.get("slug"),
            waba_account_id=data.get("waba_account_id"),
            sheet_id=data.get("sheet_id"),
            sheet_range=data.get("sheet_range"),
            estado=data.get("estado", "activo"),
            create_context=True,
        )
        return created(cliente_to_dict(c))
    except ValueError as ve:
        return error(str(ve), code="VALIDATION_ERROR", status=400)
    except IntegrityError as ie:
        return error("Conflicto de integridad", code="CONFLICT", details=str(ie.orig), status=409)
    except Exception as e:
        return error("Error no controlado al crear cliente", code="INTERNAL_ERROR", details=str(e), status=500)

def get_cliente(cliente_id: int):
    c = Cliente.query.get(cliente_id)
    if not c:
        return error("Cliente no encontrado", code="NOT_FOUND", status=404)
    return success(cliente_to_dict(c))
