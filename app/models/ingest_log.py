# app/models/ingest_log.py
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.extensions import db

class IngestLog(db.Model):
    __tablename__ = 'ingest_logs'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Tenancy y referencias
    cliente_id  = db.Column(UUID(as_uuid=True), db.ForeignKey('clientes.id'), index=True, nullable=False)
    snapshot_id = db.Column(UUID(as_uuid=True), db.ForeignKey('catalog_snapshots.id'), index=True, nullable=False)

    # Identificación de la corrida de ingesta
    run_id  = db.Column(db.String(64), nullable=False, index=True)
    origen  = db.Column(db.String(32), nullable=False)  # "webhook" | "scraper"

    # Datos/errores (JSONB reales)
    urls_json         = db.Column(JSONB, default=list)   # lista de URLs (si scraper)
    errores_json      = db.Column(JSONB, default=dict)   # errores por fila o globales
    divergencias_json = db.Column(JSONB, default=dict)   # p.ej. {"SKU123": {...}}

    # Métricas
    filas_extraidas = db.Column(db.Integer, default=0)
    pct_stock       = db.Column(db.Float)

    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    # Relaciones
    cliente  = db.relationship('Cliente', back_populates='ingest_logs')
    snapshot = db.relationship('CatalogSnapshot', back_populates='ingest_logs')

    __table_args__ = (
        # Evita duplicar corridas para el mismo cliente
        db.UniqueConstraint('cliente_id', 'run_id', name='uq_ingest_cliente_run'),
        # Consultas típicas por tenant + fecha
        db.Index('ix_ingest_cliente_created', 'cliente_id', 'created_at'),
    )

