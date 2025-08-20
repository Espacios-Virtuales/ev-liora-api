# app/controllers/usuarios_controller.py
from __future__ import annotations
from flask import Blueprint, request, g
from sqlalchemy.exc import IntegrityError
from app.views.responses import success, created, error
from app.services.core.context_service import resolve_tenant
from app.services.auth_service import crear_usuario_en_cliente, listar_usuarios_de_cliente
from app.views.serializers import usuario_to_dict

bp = Blueprint("usuarios", __name__)

def post_usuarios_en_cliente(cliente_id: int):
    """
    Alta de usuario dentro de un cliente.
    """
    # opcional: reafirmar tenant por header X-Client-ID
    try:
        resolve_tenant()
        if hasattr(g, "cliente_id") and g.cliente_id != cliente_id:
            return error("X-Client-ID no coincide con cliente_id del path", status=400)
    except Exception:
        # si no usas X-Client-ID para este endpoint, puedes omitir resolve_tenant()
        pass

    data = request.get_json(silent=True) or {}
    missing = [k for k in ("nombre", "email", "membresia_id") if not data.get(k)]
    if missing:
        return error("Datos inválidos", code="VALIDATION_ERROR", details={"missing": missing}, status=422)

    try:
        u = crear_usuario_en_cliente(
            nombre=data["nombre"],
            email=data["email"],
            membresia_id=data["membresia_id"],
            documento_id=data.get("documento_id"),
            cliente_id=cliente_id,
            waba_account_id=data.get("waba_account_id"),
            create_context=True,
        )
        return created(usuario_to_dict(u))
    except ValueError as ve:
        return error(str(ve), code="VALIDATION_ERROR", status=400)
    except IntegrityError as ie:
        return error("Conflicto de integridad", code="CONFLICT", details=str(ie.orig), status=409)
    except Exception as e:
        return error("Error no controlado al crear usuario", code="INTERNAL_ERROR", details=str(e), status=500)


def get_usuarios_de_cliente(cliente_id: int):
    """
    Listar usuarios del cliente.
    """
    try:
        resolve_tenant()
        if hasattr(g, "cliente_id") and g.cliente_id != cliente_id:
            return error("X-Client-ID no coincide con cliente_id del path", status=400)
    except Exception:
        pass

    users = listar_usuarios_de_cliente(cliente_id=cliente_id)
    return success([usuario_to_dict(u) for u in users])
