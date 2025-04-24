# app/services/documento_service.py

from app import db
from app.models.documento import Documento

def crear_documento(titulo, enlace):
    if not titulo or not enlace:
        raise ValueError("Faltan datos obligatorios.")

    if Documento.query.filter_by(titulo=titulo).first():
        raise ValueError("El documento ya existe.")

    nuevo_documento = Documento(titulo=titulo, enlace=enlace)
    db.session.add(nuevo_documento)
    db.session.commit()
    return nuevo_documento

def obtener_todos_documentos():
    return Documento.query.all()
