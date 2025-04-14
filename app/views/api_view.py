from flask import Blueprint, request
from app.controllers.bot_controller import process_request

api_bp = Blueprint("api", __name__)

@api_bp.route("/webhook", methods=["POST"])
def webhook():
    token = request.args.get("token", "")
    data = request.json
    respuesta = process_request(data, token)
    return {"respuesta": respuesta}, 200
