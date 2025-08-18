# app/controllers/usuarios_controller.py

from flask import request, jsonify
from app.services.auth_service import crear_usuario, obtener_todos_usuarios

def registrar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    membresia_id = data.get('membresia_id')
    documento_id = data.get('documento_id')

    # Validar campos obligatorios
    if not all([nombre, email, membresia_id]):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    try:
        nuevo_usuario = crear_usuario(nombre, email, membresia_id, documento_id)
        return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

def obtener_usuarios():
    usuarios = obtener_todos_usuarios()
    resultado = []
    for usuario in usuarios:
        resultado.append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'email': usuario.email,
            'membresia': usuario.membresia.nombre,
            'documento': usuario.documento.titulo if usuario.documento else None
        })
    return jsonify(resultado), 200
