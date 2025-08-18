# app/services/auth_service.py
from typing import Optional
from flask import g
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Usuario, Membresia, Documento, UserContext

def _cid(explicit: Optional[int]) -> int:
    cid = explicit or getattr(g, "cliente_id", None)
    if cid is None:
        raise ValueError("cliente_id requerido (o resolver con context_service antes).")
    return cid

def crear_usuario_en_cliente(
    nombre: str,
    email: str,
    membresia_id: int,
    documento_id: Optional[int] = None,
    cliente_id: Optional[int] = None,
    waba_account_id: Optional[int] = None,
    create_context: bool = True,
) -> Usuario:
    cid = _cid(cliente_id)

    m = Membresia.query.get(membresia_id)
    if not m:
        raise ValueError("Membresía no encontrada.")

    d = None
    if documento_id is not None:
        d = Documento.query.get(documento_id)
        if not d:
            raise ValueError("Documento no encontrado.")

    # Unicidad por cliente
    if Usuario.query.filter_by(email=email, cliente_id=cid).first():
        raise ValueError("Ya existe un usuario con ese email en este cliente.")

    u = Usuario(
        nombre=nombre,
        email=email,
        membresia_id=membresia_id,
        documento_id=d.id if d else None,
        cliente_id=cid,
        waba_account_id=waba_account_id,
    )

    try:
        db.session.add(u)
        db.session.flush()
        if create_context:
            db.session.add(UserContext(usuario_id=u.id, cliente_id=cid))
        db.session.commit()
        return u
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Conflicto de integridad al crear usuario: {e.orig}")

def listar_usuarios_de_cliente(cliente_id: Optional[int] = None) -> list[Usuario]:
    cid = _cid(cliente_id)
    return Usuario.query.filter_by(cliente_id=cid).all()
