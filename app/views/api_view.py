# app/views/api_view.py
from __future__ import annotations
from flask import Blueprint, request

from .responses import success, created, error  # mantenemos por si agregas rutas locales
from .serializers import usuario_to_dict, cliente_to_dict, waba_account_to_dict  # opcional si haces serialización aquí

# Controladores (todos devuelven (Response, status))
from app.controllers.clientes_controller import post_clientes, get_cliente
from app.controllers.usuarios_controller import post_usuarios_en_cliente, get_usuarios_de_cliente
from app.controllers.membresia_controller import registrar_membresia, obtener_membresias
from app.controllers.documento_controller import registrar_documento, obtener_documentos
from app.controllers.meta_webhook_controller import verify as meta_verify, events as meta_events
from app.controllers.waba_controller import (
    post_waba, get_waba_list, get_waba_detail, patch_waba, delete_waba,
    attach_cliente_waba, detach_cliente_waba
)

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# ----------------------
# Clientes
# ----------------------
@api_v1.route("/clientes", methods=["POST"])
def api_post_clientes():
    return post_clientes()

@api_v1.route("/clientes/<int:cliente_id>", methods=["GET"])
def api_get_cliente(cliente_id: int):
    return get_cliente(cliente_id)

# ----------------------
# Usuarios (scoped por cliente)
# ----------------------
@api_v1.route("/clientes/<int:cliente_id>/usuarios", methods=["POST"])
def api_post_usuarios(cliente_id: int):
    return post_usuarios_en_cliente(cliente_id)

@api_v1.route("/clientes/<int:cliente_id>/usuarios", methods=["GET"])
def api_get_usuarios(cliente_id: int):
    return get_usuarios_de_cliente(cliente_id)

# ----------------------
# Membresías
# ----------------------
@api_v1.route("/membresias", methods=["POST"])
def api_post_membresias():
    data = request.get_json(silent=True) or {}
    return registrar_membresia(data)

@api_v1.route("/membresias", methods=["GET"])
def api_get_membresias():
    return obtener_membresias()

# ----------------------
# Documentos
# ----------------------
@api_v1.route("/documentos", methods=["POST"])
def api_post_documentos():
    data = request.get_json(silent=True) or {}
    return registrar_documento(data)

@api_v1.route("/documentos", methods=["GET"])
def api_get_documentos():
    return obtener_documentos()

# ----------------------
# WABA (CRUD backoffice)
# ----------------------
@api_v1.route("/waba", methods=["POST"])
def api_post_waba():
    return post_waba()

@api_v1.route("/waba", methods=["GET"])
def api_get_waba_list():
    return get_waba_list()

@api_v1.route("/waba/<int:waba_id>", methods=["GET"])
def api_get_waba_detail(waba_id: int):
    return get_waba_detail(waba_id)

@api_v1.route("/waba/<int:waba_id>", methods=["PATCH"])
def api_patch_waba(waba_id: int):
    return patch_waba(waba_id)

@api_v1.route("/waba/<int:waba_id>", methods=["DELETE"])
def api_delete_waba(waba_id: int):
    return delete_waba(waba_id)

# ----------------------
# WABA ↔ Cliente (tenant)
# ----------------------
@api_v1.route("/clientes/<int:cliente_id>/waba", methods=["POST"])
def api_attach_cliente_waba(cliente_id: int):
    return attach_cliente_waba(cliente_id)

@api_v1.route("/clientes/<int:cliente_id>/waba", methods=["DELETE"])
def api_detach_cliente_waba(cliente_id: int):
    return detach_cliente_waba(cliente_id)

# ----------------------
# Webhook Meta (renombrado desde wsp_controller)
# ----------------------
@api_v1.route("/webhook/meta", methods=["GET"])
def api_webhook_meta_verify():
    return meta_verify()

@api_v1.route("/webhook/meta", methods=["POST"])
def api_webhook_meta_events():
    return meta_events()
