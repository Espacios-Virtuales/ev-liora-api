import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class UserContext(db.Model):
    __tablename__ = "user_contexts"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"),
                           unique=True, nullable=False)
    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey("clientes.id"),
                           nullable=False, index=True)
    msisdn = db.Column(db.String(30))
    last_intent = db.Column(db.String(50))
    slots_json = db.Column(db.JSON, default={})
    context_json = db.Column(db.JSON, default={})
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
