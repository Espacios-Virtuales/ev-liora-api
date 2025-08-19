# app/services/documento_service.py
from __future__ import annotations
from app.extensions import db
from app.models.documento import Documento

def crear_documento(titulo: str, enlace: str) -> Documento:
    if not titulo or not enlace:
        raise ValueError("Faltan datos obligatorios (titulo, enlace).")
    if Documento.query.filter_by(titulo=titulo).first():
        raise ValueError("El documento ya existe.")
    d = Documento(titulo=titulo, enlace=enlace)
    db.session.add(d)
    db.session.commit()
    return d

def obtener_todos_documentos() -> list[Documento]:
    return Documento.query.order_by(Documento.id.desc()).all()
