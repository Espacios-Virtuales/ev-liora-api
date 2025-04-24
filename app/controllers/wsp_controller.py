from flask import request, jsonify
from app.services import whatsapp_service

def registrar_numero_whatsapp():
    data = request.get_json()
    nuevo_numero = whatsapp_service.crear_numero_whatsapp(data)
    return jsonify({'mensaje': 'Número de WhatsApp registrado exitosamente', 'id': nuevo_numero.id}), 201

def obtener_numeros_whatsapp():
    numeros = whatsapp_service.obtener_numeros_whatsapp()
    resultado = []
    for numero in numeros:
        resultado.append({
            'id': numero.id,
            'numero': numero.numero,
            'waba_id': numero.waba_id,
            'phone_number_id': numero.phone_number_id,
            'token': numero.token,
            'webhook_url': numero.webhook_url,
            'estado': numero.estado
        })
    return jsonify(resultado), 200

def obtener_numero_whatsapp(numero_id):
    numero = whatsapp_service.obtener_numero_whatsapp_por_id(numero_id)
    if not numero:
        return jsonify({'error': 'Número de WhatsApp no encontrado'}), 404
    resultado = {
        'id': numero.id,
        'numero': numero.numero,
        'waba_id': numero.waba_id,
        'phone_number_id': numero.phone_number_id,
        'token': numero.token,
        'webhook_url': numero.webhook_url,
        'estado': numero.estado
    }
    return jsonify(resultado), 200

def actualizar_numero_whatsapp(numero_id):
    data = request.get_json()
    numero_actualizado = whatsapp_service.actualizar_numero_whatsapp(numero_id, data)
    if not numero_actualizado:
        return jsonify({'error': 'Número de WhatsApp no encontrado'}), 404
    return jsonify({'mensaje': 'Número de WhatsApp actualizado exitosamente'}), 200

def eliminar_numero_whatsapp(numero_id):
    numero_eliminado = whatsapp_service.eliminar_numero_whatsapp(numero_id)
    if not numero_eliminado:
        return jsonify({'error': 'Número de WhatsApp no encontrado'}), 404
    return jsonify({'mensaje': 'Número de WhatsApp eliminado exitosamente'}), 200
