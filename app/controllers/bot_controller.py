from flask import Flask, request, jsonify
from app.services.sheet_service import cargar_datos_hoja, procesar_pregunta

app = Flask(__name__)

@app.route('/responder', methods=['POST'])
def responder():
    data = request.get_json()
    pregunta = data.get('pregunta')
    documento_id = data.get('documento_id')

    if not pregunta or not documento_id:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    try:
        sheet_data = cargar_datos_hoja(documento_id)
        respuesta = procesar_pregunta(pregunta, sheet_data)
        return jsonify({'respuesta': respuesta}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
