from flask import request, jsonify
from app.models.db_models import db, Documento

def registrar_documento():
    data = request.get_json()
    titulo = data.get('titulo')
    enlace = data.get('enlace')

    if not all([titulo, enlace]):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    if Documento.query.filter_by(titulo=titulo).first():
        return jsonify({'error': 'El documento ya existe'}), 409

    nuevo_documento = Documento(titulo=titulo, enlace=enlace)
    db.session.add(nuevo_documento)
    db.session.commit()

    return jsonify({'mensaje': 'Documento registrado exitosamente'}), 201

def obtener_documentos():
    documentos = Documento.query.all()
    resultado = []
    for d in documentos:
        resultado.append({
            'id': d.id,
            'nombre': d.nombre,
            'enlace': d.enlace,
        })
    return jsonify(resultado), 200
