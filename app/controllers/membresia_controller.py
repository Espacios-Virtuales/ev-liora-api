# app/controllers/membresia_controller.py

from flask import request, jsonify
from app.services.membresia_service import crear_membresia, obtener_todas_membresias

def registrar_membresia():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    try:
        nueva_membresia = crear_membresia(nombre, descripcion)
        return jsonify({'mensaje': 'Membresía registrada exitosamente'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

def obtener_membresias():
    membresias = obtener_todas_membresias()
    resultado = [
        {
            'id': m.id,
            'nombre': m.nombre,
            'descripcion': m.descripcion
        } for m in membresias
    ]
    return jsonify(resultado), 200
