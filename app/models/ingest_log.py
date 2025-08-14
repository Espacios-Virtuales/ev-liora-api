# app/models/ingest_log.py
from app.extensions import db

class IngestLog(db.Model):
    __tablename__ = 'ingest_logs'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False, index=True)
    run_id = db.Column(db.String(64), nullable=False, index=True)
    origen = db.Column(db.String(32), nullable=False) # "webhook" | "scraper"
    urls_json = db.Column(db.JSON)        # lista de URLs si aplica (scraping)
    errores_json = db.Column(db.JSON)     # errores por fila o generales
    divergencias_json = db.Column(db.JSON) # {"SKU123": {"campo":"precio", "oficial": 10, "scraper": 12}}
    filas_extraidas = db.Column(db.Integer, default=0)
    pct_stock = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    cliente = db.relationship('Cliente', back_populates='ingest_logs')
