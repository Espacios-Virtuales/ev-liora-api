from flask import request, jsonify
from app.models.db_models import db, Usuario, Membresia, Documento

from flask import request, jsonify
from app.models.db_models import db, Usuario, Membresia, Documento

def registrar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    membresia_id = data.get('membresia_id')
    documento_id = data.get('documento_id')

    # Validar campos obligatorios
    if not all([nombre, email, membresia_id]):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    # Verificar existencia de la membresía
    membresia = Membresia.query.get(membresia_id)
    if not membresia:
        return jsonify({'error': 'Membresía no encontrada'}), 404

    # Verificar existencia del documento si se proporciona
    documento = None
    if documento_id:
        documento = Documento.query.get(documento_id)
        if not documento:
            return jsonify({'error': 'Documento no encontrado'}), 404

    # Crear y guardar el nuevo usuario
    nuevo_usuario = Usuario(
        nombre=nombre,
        email=email,
        membresia_id=membresia_id,
        documento_id=documento_id if documento else None
    )
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
