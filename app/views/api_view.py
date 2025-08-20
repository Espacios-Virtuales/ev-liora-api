# app/views/api_view.py
from __future__ import annotations
# 🔹 CAMBIO: usar el Blueprint de flask_smorest
from flask_smorest import Blueprint
from flask import request

# Mantén tus helpers si quieres usarlos en controladores
from .responses import success, created, error  # opcional
from .serializers import usuario_to_dict, cliente_to_dict, waba_account_to_dict  # opcional

# Controladores (devuelven (Response, status))
from app.controllers.clientes_controller import post_clientes, get_cliente
from app.controllers.usuarios_controller import post_usuarios_en_cliente, get_usuarios_de_cliente
from app.controllers.membresia_controller import registrar_membresia, obtener_membresias
from app.controllers.documento_controller import registrar_documento, obtener_documentos
from app.controllers.meta_webhook_controller import verify as meta_verify, events as meta_events
from app.controllers.waba_controller import (
    post_waba, get_waba_list, get_waba_detail, patch_waba, delete_waba,
    attach_cliente_waba, detach_cliente_waba
)

# 🔹 CAMBIO: smorest.Blueprint
api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1", description="API pública v1")

# ----------------------
# Clientes
# ----------------------
@api_v1.route("/clientes", methods=["POST"])
@api_v1.response(201, description="Cliente creado")
def api_post_clientes():
    """Crear cliente"""
    return post_clientes()

@api_v1.route("/clientes/<int:cliente_id>", methods=["GET"])
@api_v1.response(200, description="Detalle de cliente")
@api_v1.doc(parameters=[{"in": "path", "name": "cliente_id", "schema": {"type": "integer"}}])
def api_get_cliente(cliente_id: int):
    """Obtener cliente por id"""
    return get_cliente(cliente_id)

# ----------------------
# Usuarios (scoped por cliente)
# ----------------------
@api_v1.route("/clientes/<int:cliente_id>/usuarios", methods=["POST"])
@api_v1.response(201, description="Usuario creado en cliente")
@api_v1.doc(parameters=[{"in": "path", "name": "cliente_id", "schema": {"type": "integer"}}])
def api_post_usuarios(cliente_id: int):
    """Crear usuario en cliente"""
    return post_usuarios_en_cliente(cliente_id)

@api_v1.route("/clientes/<int:cliente_id>/usuarios", methods=["GET"])
@api_v1.response(200, description="Listado de usuarios del cliente")
@api_v1.doc(parameters=[{"in": "path", "name": "cliente_id", "schema": {"type": "integer"}}])
def api_get_usuarios(cliente_id: int):
    """Listar usuarios de un cliente"""
    return get_usuarios_de_cliente(cliente_id)

# ----------------------
# Membresías
# ----------------------
@api_v1.route("/membresias", methods=["POST"])
@api_v1.response(201, description="Membresía registrada")
def api_post_membresias():
    """Registrar membresía"""
    data = request.get_json(silent=True) or {}
    return registrar_membresia(data)

@api_v1.route("/membresias", methods=["GET"])
@api_v1.response(200, description="Listado de membresías")
def api_get_membresias():
    """Listar membresías"""
    return obtener_membresias()

# ----------------------
# Documentos
# ----------------------
@api_v1.route("/documentos", methods=["POST"])
@api_v1.response(201, description="Documento registrado")
def api_post_documentos():
    """Registrar documento"""
    data = request.get_json(silent=True) or {}
    return registrar_documento(data)

@api_v1.route("/documentos", methods=["GET"])
@api_v1.response(200, description="Listado de documentos")
def api_get_documentos():
    """Listar documentos"""
    return obtener_documentos()

# ----------------------
# WABA (CRUD backoffice)
# ----------------------
@api_v1.route("/waba", methods=["POST"])
@api_v1.response(201, description="WABA creado/registrado")
def api_post_waba():
    """Crear/registrar WABA"""
    return post_waba()

@api_v1.route("/waba", methods=["GET"])
@api_v1.response(200, description="Listado WABA")
def api_get_waba_list():
    """Listar WABA"""
    return get_waba_list()

@api_v1.route("/waba/<int:waba_id>", methods=["GET"])
@api_v1.response(200, description="Detalle WABA")
@api_v1.doc(parameters=[{"in": "path", "name": "waba_id", "schema": {"type": "integer"}}])
def api_get_waba_detail(waba_id: int):
    """Obtener WABA por id"""
    return get_waba_detail(waba_id)

@api_v1.route("/waba/<int:waba_id>", methods=["PATCH"])
@api_v1.response(200, description="WABA actualizado")
@api_v1.doc(parameters=[{"in": "path", "name": "waba_id", "schema": {"type": "integer"}}])
def api_patch_waba(waba_id: int):
    """Actualizar WABA"""
    return patch_waba(waba_id)

@api_v1.route("/waba/<int:waba_id>", methods=["DELETE"])
@api_v1.response(204, description="WABA eliminado")
@api_v1.doc(parameters=[{"in": "path", "name": "waba_id", "schema": {"type": "integer"}}])
def api_delete_waba(waba_id: int):
    """Eliminar WABA"""
    return delete_waba(waba_id)

# ----------------------
# WABA ↔ Cliente (tenant)
# ----------------------
@api_v1.route("/clientes/<int:cliente_id>/waba", methods=["POST"])
@api_v1.response(200, description="WABA asociado al cliente")
@api_v1.doc(parameters=[{"in": "path", "name": "cliente_id", "schema": {"type": "integer"}}])
def api_attach_cliente_waba(cliente_id: int):
    """Asociar WABA a cliente"""
    return attach_cliente_waba(cliente_id)

@api_v1.route("/clientes/<int:cliente_id>/waba", methods=["DELETE"])
@api_v1.response(204, description="WABA desasociado del cliente")
@api_v1.doc(parameters=[{"in": "path", "name": "cliente_id", "schema": {"type": "integer"}}])
def api_detach_cliente_waba(cliente_id: int):
    """Desasociar WABA de cliente"""
    return detach_cliente_waba(cliente_id)

# ----------------------
# Webhook Meta (renombrado desde wsp_controller)
# ----------------------
@api_v1.route("/webhook/meta", methods=["GET"])
@api_v1.response(200, description="Verificación webhook (challenge)")
def api_webhook_meta_verify():
    """Responder hub.challenge de Meta"""
    return meta_verify()

@api_v1.route("/webhook/meta", methods=["POST"])
@api_v1.response(200, description="Evento de webhook recibido")
def api_webhook_meta_events():
    """Eventos entrantes desde Meta (WhatsApp Cloud API)"""
    return meta_events()
