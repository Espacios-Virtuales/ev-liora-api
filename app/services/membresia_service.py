# app/services/membresia_service.py

from app import db
from app.models.membresia import Membresia

def crear_membresia(nombre, descripcion=None):
    if not nombre:
        raise ValueError("El nombre es obligatorio.")

    if Membresia.query.filter_by(nombre=nombre).first():
        raise ValueError("La membresía ya existe.")

    nueva_membresia = Membresia(nombre=nombre, descripcion=descripcion)
    db.session.add(nueva_membresia)
    db.session.commit()
    return nueva_membresia

def obtener_todas_membresias():
    return Membresia.query.all()
