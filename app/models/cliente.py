# app/models/cliente.py
from app.extensions import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    waba_account_id = db.Column(db.Integer, db.ForeignKey('waba_accounts.id'), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(80), unique=True, index=True)  # p.ej. "tienda‑andina"
    estado = db.Column(db.String(32), default='activo')

    # Fuente de datos del cliente (opcional si usan Sheets)
    sheet_id = db.Column(db.String(128))
    sheet_range = db.Column(db.String(128))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relaciones
    waba_account = db.relationship('WabaAccount', back_populates='clientes')
    catalog_active = db.relationship('CatalogActive', uselist=False, back_populates='cliente', cascade='all, delete-orphan')
    snapshots = db.relationship('CatalogSnapshot', back_populates='cliente', cascade='all, delete-orphan')
    ingest_logs = db.relationship('IngestLog', back_populates='cliente', cascade='all, delete-orphan')
    convo_states = db.relationship('ConvoState', back_populates='cliente', cascade='all, delete-orphan')
    conversation_logs = db.relationship('ConversationLog', back_populates='cliente', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Cliente {self.slug or self.nombre}>"
