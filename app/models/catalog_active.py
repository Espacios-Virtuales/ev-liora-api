# app/models/catalog_active.py
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.extensions import db

class CatalogActive(db.Model):
    __tablename__ = 'catalog_active'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey('clientes.id'), unique=True, nullable=False)
    version = db.Column(db.String(64), nullable=False)
    checksum = db.Column(db.String(128), nullable=False)
    rows = db.Column(db.Integer, default=0)
    pct_stock = db.Column(db.Float)  # porcentaje de items con stock
    activated_at = db.Column(db.DateTime, server_default=db.func.now())

    # Copia del esquema normalizado (opcional), para lecturas rápidas
    meta_json = db.Column(db.JSON)

    cliente = db.relationship('Cliente', back_populates='catalog_active')






