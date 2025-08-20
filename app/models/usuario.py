# app/models/usuario.py
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Multi-tenant: usuario pertenece a un cliente
    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey('clientes.id'), index=True, nullable=True)
    cliente = db.relationship("Cliente", backref="usuarios", lazy=True)

    # (Opcional) vínculo a WABA (si lo usas)
    waba_account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('waba_accounts.id'), nullable=True)

    # Timestamps (útiles para auditoría)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 1:1 – si usas UserContext
    context = db.relationship(
        "UserContext",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # 1:N – Usuario → Documentos (el hijo tiene FK usuario_id)
    documentos = db.relationship(
        "Documento",
        back_populates="usuario",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # 1:N – Usuario → Membresías (el hijo tiene FK usuario_id)
    membresias = db.relationship(
        "Membresia",
        back_populates="usuario",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Usuario {self.email}>"

