from flask import request, jsonify
from app.services.chat_service import cargar_entradas_desde_sheet, buscar_respuesta

def responder_pregunta():
    data = request.get_json()
    pregunta = data.get("pregunta")
    documento_id = data.get("documento_id")

    if not pregunta or not documento_id:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        entradas = cargar_entradas_desde_sheet(documento_id)
        respuesta = buscar_respuesta(pregunta, entradas)
        if respuesta:
            return jsonify({"respuesta": respuesta})
        return jsonify({"respuesta": "No encontré una respuesta en mi base de conocimientos."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
