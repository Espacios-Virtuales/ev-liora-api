from flask import request, jsonify
from app.models.db_models import db, Membresia

def registrar_membresia():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    if not nombre:
        return jsonify({'error': 'El nombre es obligatorio'}), 400

    if Membresia.query.filter_by(nombre=nombre).first():
        return jsonify({'error': 'La membresía ya existe'}), 409

    nueva_membresia = Membresia(nombre=nombre, descripcion=descripcion)
    db.session.add(nueva_membresia)
    db.session.commit()

    return jsonify({'mensaje': 'Membresía registrada exitosamente'}), 201

def obtener_membresias():
    membresias = Membresia.query.all()
    resultado = []
    for m in membresias:
        resultado.append({
            'id': m.id,
            'nombre': m.nombre,
            'descripcion': m.descripcion
        })
    return jsonify(resultado), 200
