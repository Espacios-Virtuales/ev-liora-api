import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class Documento(db.Model):
    __tablename__ = "documentos"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey("clientes.id"), index=True, nullable=True)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), index=True, nullable=False)

    titulo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), default="generic")
    cuerpo = db.Column(db.Text)
    estado = db.Column(db.String(20), default="activo")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # lado N→1 (singular en el hijo)
    usuario = db.relationship("Usuario", back_populates="documentos")
