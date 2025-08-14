# app/models/catalog_snapshot.py
from app.extensions import db

class CatalogSnapshot(db.Model):
    __tablename__ = 'catalog_snapshots'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False, index=True)
    version = db.Column(db.String(64), nullable=False, index=True)
    origen = db.Column(db.String(32), nullable=False)  # "webhook" | "scraper"
    checksum = db.Column(db.String(128), nullable=False)
    filas_validas = db.Column(db.Integer, default=0)
    errores_json = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Datos crudos opcionales (si guardas el CSV/JSON empaquetado)
    blob_url = db.Column(db.String(512))

    cliente = db.relationship('Cliente', back_populates='snapshots')

    __table_args__ = (
        db.UniqueConstraint('cliente_id', 'version', name='uq_snapshot_cliente_version'),
    )
