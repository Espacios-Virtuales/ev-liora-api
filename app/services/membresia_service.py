# app/services/membresia_service.py
from __future__ import annotations
from app.extensions import db
from app.models.membresia import Membresia

def crear_membresia(nombre: str, descripcion: str | None = None) -> Membresia:
    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if Membresia.query.filter_by(nombre=nombre).first():
        raise ValueError("La membresía ya existe.")
    m = Membresia(nombre=nombre, descripcion=descripcion)
    db.session.add(m)
    db.session.commit()
    return m

def obtener_todas_membresias() -> list[Membresia]:
    return Membresia.query.order_by(Membresia.id.desc()).all()
