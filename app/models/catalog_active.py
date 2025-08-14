# app/models/catalog_active.py
from app.extensions import db

class CatalogActive(db.Model):
    __tablename__ = 'catalog_active'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False, unique=True)
    version = db.Column(db.String(64), nullable=False)
    checksum = db.Column(db.String(128), nullable=False)
    rows = db.Column(db.Integer, default=0)
    pct_stock = db.Column(db.Float)  # porcentaje de items con stock
    activated_at = db.Column(db.DateTime, server_default=db.func.now())

    # Copia del esquema normalizado (opcional), para lecturas rápidas
    meta_json = db.Column(db.JSON)

    cliente = db.relationship('Cliente', back_populates='catalog_active')






