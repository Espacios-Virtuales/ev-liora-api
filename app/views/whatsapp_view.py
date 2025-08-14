# app/views/whatsapp_view.py
from flask import Blueprint, request, jsonify
from app.services.sheet_service import cargar_datos_hoja, procesar_pregunta

whatsapp_bp = Blueprint("whatsapp", __name__)

@whatsapp_bp.route("/whatsapp", methods=["POST"])

def recibir_mensaje():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    usuario_id = data.get("usuario_id")  # este puede venir desde la API de WSP o interno

    # Para prototipo usamos sheet fija por usuario
    sheet_id = "TU_SHEET_ID_AQUI"  # o recuperado de la BDD si es dinámico
    datos_respuestas = cargar_datos_hoja(sheet_id)
    respuesta = procesar_pregunta(mensaje, datos_respuestas)

    return jsonify({"respuesta": respuesta}), 200
