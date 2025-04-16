from flask import Blueprint, request
from app.controllers.bot_controller import process_request
from app.controllers.user_controller import registrar_usuario, obtener_usuarios


api_bp = Blueprint("api", __name__)

@api_bp.route("/webhook", methods=["POST"])
def webhook():
    token = request.args.get("token", "")
    data = request.json
    respuesta = process_request(data, token)
    return {"respuesta": respuesta}, 200


api_bp.route('/usuarios', methods=['POST'])(registrar_usuario)
api_bp.route('/usuarios', methods=['GET'])(obtener_usuarios)