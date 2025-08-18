# app/views/api_view.py
from flask import Blueprint, request, g
from .responses import success, created, error
from .serializers import usuario_to_dict, cliente_to_dict, waba_account_to_dict

# Controladores 
from app.controllers.usuarios_controller import post_usuarios_en_cliente, get_usuarios_de_cliente
from app.controllers.clientes_controller import post_clientes
from app.controllers.meta_webhook_controller import verify as meta_verify, events as meta_events
from app.controllers.membresia_controller import registrar_membresia, obtener_membresias
from app.controllers.documento_controller import registrar_documento, obtener_documentos

# Si tienes chat:
from app.controllers.chat_controller import responder_pregunta

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# ---- Clientes
@api_v1.route("/clientes", methods=["POST"])
def api_post_clientes():
    resp, status = post_clientes()  # usa el controlador que ya armamos
    return resp, status

# ---- Usuarios (por cliente)
@api_v1.route("/clientes/<int:cliente_id>/usuarios", methods=["POST"])
def api_post_usuarios(cliente_id: int):
    resp, status = post_usuarios_en_cliente(cliente_id)
    return resp, status

@api_v1.route("/clientes/<int:cliente_id>/usuarios", methods=["GET"])
def api_get_usuarios(cliente_id: int):
    resp, status = get_usuarios_de_cliente(cliente_id)
    return resp, status

# ---- Membresías
@api_v1.route("/membresias", methods=["POST"])
def api_post_membresias():
    try:
        data = request.get_json(force=True)
        obj = registrar_membresia(data)  # asumiendo tu controlador retorna objeto
        return created({"id": obj.id})
    except Exception as e:
        return error(str(e), code="VALIDATION_ERROR", status=400)

@api_v1.route("/membresias", methods=["GET"])
def api_get_membresias():
    objs = obtener_membresias()
    return success([{"id": m.id, "nombre": m.nombre} for m in objs])

# ---- Documentos
@api_v1.route("/documentos", methods=["POST"])
def api_post_documentos():
    try:
        data = request.get_json(force=True)
        obj = registrar_documento(data)
        return created({"id": obj.id})
    except Exception as e:
        return error(str(e), code="VALIDATION_ERROR", status=400)

@api_v1.route("/documentos", methods=["GET"])
def api_get_documentos():
    objs = obtener_documentos()
    return success([{"id": d.id, "nombre": d.nombre} for d in objs])

# ---- Chat
@api_v1.route("/chatbot/responder", methods=["POST"])
def api_chat_responder():
    try:
        data = request.get_json(force=True)
        r = responder_pregunta(data)
        return success(r)
    except Exception as e:
        return error(str(e), status=400)

# ---- Webhook Meta (renombrado desde wsp_controller)
@api_v1.route("/webhook/meta", methods=["GET"])
def api_webhook_meta_verify():
    return meta_verify()

@api_v1.route("/webhook/meta", methods=["POST"])
def api_webhook_meta_events():
    return meta_events()
