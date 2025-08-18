from app.models import NumeroWhatsApp, Usuario
from app.extensions import db
from flask import jsonify


def crear_numero_whatsapp(data):
    try:
        # Validar campos obligatorios
        required_fields = ['numero', 'waba_id', 'phone_number_id', 'token']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Faltan campos obligatorios: {", ".join(missing_fields)}'}), 400

        # Crear el nuevo número de WhatsApp
        nuevo_numero = NumeroWhatsApp(
            numero=data['numero'],
            waba_id=data['waba_id'],
            phone_number_id=data['phone_number_id'],
            token=data['token'],
            webhook_url=data.get('webhook_url'),
            estado=data.get('estado', 'activo')
        )
        db.session.add(nuevo_numero)
        db.session.commit()

        # Asociar el número al usuario, si se proporciona usuario_id
        usuario_id = data.get('usuario_id')
        if usuario_id:
            usuario = Usuario.query.get(usuario_id)
            if not usuario:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            usuario.numero_whatsapp_id = nuevo_numero.id
            db.session.commit()

        return nuevo_numero

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Ocurrió un error al crear el número de WhatsApp: {str(e)}'}), 500


def obtener_numeros_whatsapp():
    return NumeroWhatsApp.query.all()

def obtener_numero_whatsapp_por_id(numero_id):
    return NumeroWhatsApp.query.get(numero_id)

def actualizar_numero_whatsapp(numero_id, data):
    numero = NumeroWhatsApp.query.get(numero_id)
    if not numero:
        return None
    numero.numero = data.get('numero', numero.numero)
    numero.waba_id = data.get('waba_id', numero.waba_id)
    numero.phone_number_id = data.get('phone_number_id', numero.phone_number_id)
    numero.token = data.get('token', numero.token)
    numero.webhook_url = data.get('webhook_url', numero.webhook_url)
    numero.estado = data.get('estado', numero.estado)
    db.session.commit()
    return numero

def eliminar_numero_whatsapp(numero_id):
    numero = NumeroWhatsApp.query.get(numero_id)
    if not numero:
        return None
    db.session.delete(numero)
    db.session.commit()
    return numero
