import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class Membresia(db.Model):
    __tablename__ = "membresias"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey("clientes.id"), index=True, nullable=False)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), index=True, nullable=False)

    plan = db.Column(db.String(30), nullable=False)      # free|basic|pro
    estado = db.Column(db.String(20), default="activa")  # activa|suspendida|cancelada
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime)

    usuario = db.relationship("Usuario", back_populates="membresias")
