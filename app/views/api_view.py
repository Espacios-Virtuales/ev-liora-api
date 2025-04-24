from flask import Blueprint
from app.controllers.chat_controller import responder_pregunta
from app.controllers.user_controller import registrar_usuario, obtener_usuarios
from app.controllers.membresia_controller import registrar_membresia, obtener_membresias
from app.controllers.documento_controller import registrar_documento, obtener_documentos
from app.controllers import numero_whatsapp_controller


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

# Números de WhatsApp
api_bp.route('/numeros_whatsapp', methods=['POST'])(numero_whatsapp_controller.registrar_numero_whatsapp)
api_bp.route('/numeros_whatsapp', methods=['GET'])(numero_whatsapp_controller.obtener_numeros_whatsapp)
api_bp.route('/numeros_whatsapp/<int:numero_id>', methods=['GET'])(numero_whatsapp_controller.obtener_numero_whatsapp)
api_bp.route('/numeros_whatsapp/<int:numero_id>', methods=['PUT'])(numero_whatsapp_controller.actualizar_numero_whatsapp)
api_bp.route('/numeros_whatsapp/<int:numero_id>', methods=['DELETE'])(numero_whatsapp_controller.eliminar_numero_whatsapp)