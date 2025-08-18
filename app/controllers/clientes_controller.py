# app/controllers/clientes_controller.py
from flask import Blueprint, request, jsonify
from app.services.core.security import requires_tenant  # si decides proteger este recurso
from app.services.cliente_service import crear_cliente

bp = Blueprint("clientes", __name__)

@bp.route("/clientes", methods=["POST"])
def post_clientes():
    """
    Alta de cliente (admin/backoffice). Si tu modelo de seguridad lo requiere,
    protege este endpoint con un rol de 'admin' global.
    """
    data = request.get_json(force=True)
    try:
        cliente = crear_cliente(
            nombre=data.get("nombre"),
            slug=data.get("slug"),
            waba_account_id=data.get("waba_account_id"),
            sheet_id=data.get("sheet_id"),
            sheet_range=data.get("sheet_range"),
            estado=data.get("estado", "activo"),
            create_context=True,
        )
        return jsonify({
            "id": cliente.id,
            "slug": cliente.slug,
            "nombre": cliente.nombre,
            "estado": cliente.estado
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
