from flask import request, jsonify
from app.models.db_models import db, Usuario, Membresia, Documento

def registrar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    membresia_id = data.get('membresia_id')
    documento_id = data.get('documento_id')

    if not all([nombre, email, membresia_id]):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    nuevo_usuario = Usuario(nombre=nombre, email=email, membresia_id=membresia_id, documento_id=documento_id)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201

def obtener_usuarios():
    usuarios = Usuario.query.all()
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
