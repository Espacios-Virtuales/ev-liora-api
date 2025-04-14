from flask import Blueprint, request
from app.controllers.bot_controller import process_message

whatsapp_bp = Blueprint("whatsapp", __name__)

@whatsapp_bp.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    mensaje = data.get("message", "")
    respuesta = process_message(mensaje)
    return {"respuesta": respuesta}, 200
