# app/services/cliente_service.py
from typing import Optional
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Cliente, ClientContext, WabaAccount

def _slugify(nombre: str) -> str:
    base = (nombre or "").strip().lower().replace(" ", "-")
    return "".join(ch for ch in base if ch.isalnum() or ch in "-_")[:80]

def crear_cliente(
    nombre: str,
    slug: Optional[str] = None,
    waba_account_id: Optional[int] = None,
    sheet_id: Optional[str] = None,
    sheet_range: Optional[str] = None,
    estado: str = "activo",
    create_context: bool = True,
) -> Cliente:
    slug = slug or _slugify(nombre)
    if not slug:
        raise ValueError("El slug/nombre del cliente es requerido.")

    # Validar WABA si se entrega
    waba = None
    if waba_account_id is not None:
        waba = WabaAccount.query.get(waba_account_id)
        if not waba:
            raise ValueError("WabaAccount no encontrada.")

    # Unicidad de slug
    if Cliente.query.filter_by(slug=slug).first():
        raise ValueError("Ya existe un cliente con ese slug.")

    cliente = Cliente(
        nombre=nombre,
        slug=slug,
        waba_account_id=waba.id if waba else None,
        sheet_id=sheet_id,
        sheet_range=sheet_range,
        estado=estado,
    )

    try:
        db.session.add(cliente)
        db.session.flush()

        if create_context:
            ctx = ClientContext(cliente_id=cliente.id)
            db.session.add(ctx)

        db.session.commit()
        return cliente

    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Conflicto de integridad al crear cliente: {e.orig}")
