# app/controllers/usuarios_controller.py
from flask import Blueprint, request, jsonify, g
from app.services.core.security import requires_tenant
from app.services.core.context_service import resolve_tenant
from app.services.auth_service import crear_usuario_en_cliente, listar_usuarios_de_cliente

bp = Blueprint("usuarios", __name__)

@bp.route("/clientes/<int:cliente_id>/usuarios", methods=["POST"])
def post_usuarios_en_cliente(cliente_id: int):
    """
    Alta de usuario dentro del cliente indicado.
    Si usas header X-Client-ID, puedes llamar resolve_tenant() para setear g.cliente_id
    y cross-check contra el path.
    """
    resolve_tenant()  # opcional si usas X-Client-ID; asegura g.cliente_id
    if hasattr(g, "cliente_id") and g.cliente_id != cliente_id:
        return jsonify({"error": "X-Client-ID no coincide con cliente_id del path"}), 400

    data = request.get_json(force=True)
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
        return jsonify({
            "id": u.id,
            "email": u.email,
            "cliente_id": u.cliente_id
        }), 201
    except KeyError as e:
        return jsonify({"error": f"Falta campo requerido: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/clientes/<int:cliente_id>/usuarios", methods=["GET"])
def get_usuarios_de_cliente(cliente_id: int):
    resolve_tenant()  # opcional
    if hasattr(g, "cliente_id") and g.cliente_id != cliente_id:
        return jsonify({"error": "X-Client-ID no coincide con cliente_id del path"}), 400

    usuarios = listar_usuarios_de_cliente(cliente_id=cliente_id)
    return jsonify([
        {"id": u.id, "email": u.email, "nombre": u.nombre}
        for u in usuarios
    ])
