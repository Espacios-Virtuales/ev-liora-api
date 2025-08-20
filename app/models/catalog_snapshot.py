# app/models/catalog_snapshot.py
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.extensions import db

class CatalogSnapshot(db.Model):
    __tablename__ = 'catalog_snapshots'

    id          = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id  = db.Column(UUID(as_uuid=True), db.ForeignKey('clientes.id'), nullable=False, index=True)
    version     = db.Column(db.String(64), nullable=False)
    origen      = db.Column(db.String(32), nullable=False)   # "webhook" | "scraper"
    checksum    = db.Column(db.String(128), nullable=False)
    filas_validas  = db.Column(db.Integer, default=0)
    errores_json   = db.Column(JSONB, default=dict)          # ← JSONB real
    created_at     = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    blob_url       = db.Column(db.String(512))               # opcional: URL al dump/CSV

    # Relaciones
    cliente = db.relationship('Cliente', back_populates='snapshots')
    ingest_logs = db.relationship('IngestLog', back_populates='snapshot',
                                  cascade='all, delete-orphan')

    __table_args__ = (
        # Único por cliente+versión
        db.UniqueConstraint('cliente_id', 'version', name='uq_snapshot_cliente_version'),
        # Índice útil para listar por tenant y fecha
        db.Index('ix_snapshot_cliente_created', 'cliente_id', 'created_at'),
    )
