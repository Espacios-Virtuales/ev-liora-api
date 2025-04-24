# app/controllers/documento_controller.py

from flask import request, jsonify
from app.services.documento_service import crear_documento, obtener_todos_documentos

def registrar_documento():
    data = request.get_json()
    titulo = data.get('titulo')
    enlace = data.get('enlace')

    try:
        nuevo_documento = crear_documento(titulo, enlace)
        return jsonify({'mensaje': 'Documento registrado exitosamente'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

def obtener_documentos():
    documentos = obtener_todos_documentos()
    resultado = [
        {
            'id': d.id,
            'titulo': d.titulo,
            'enlace': d.enlace
        } for d in documentos
    ]
    return jsonify(resultado), 200
