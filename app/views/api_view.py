from flask import Blueprint
from app.controllers.chat_controller import responder_pregunta
from app.controllers.user_controller import registrar_usuario, obtener_usuarios
from app.controllers.membresia_controller import registrar_membresia, obtener_membresias
from app.controllers.documento_controller import registrar_documento, obtener_documentos

api_bp = Blueprint("api", __name__)

# Usuarios
api_bp.route('/usuarios', methods=['POST'])(registrar_usuario)
api_bp.route('/usuarios', methods=['GET'])(obtener_usuarios)

# Membresías
api_bp.route('/membresias', methods=['POST'])(registrar_membresia)
api_bp.route('/membresias', methods=['GET'])(obtener_membresias)

# Documentos
api_bp.route('/documentos', methods=['POST'])(registrar_documento)
api_bp.route('/documentos', methods=['GET'])(obtener_documentos)


# Responder
api_bp.route('/chatbot/responder',  methods=['POST'])(responder_pregunta)
