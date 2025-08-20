# app/models/user_context.py
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.extensions import db


class UserContext(db.Model):
    __tablename__ = "user_contexts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # FK correctas (UUID)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), nullable=False, unique=True)
    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey("clientes.id"), nullable=False, index=True)

    msisdn = db.Column(db.String(30))
    last_intent = db.Column(db.String(50))

    # JSONB reales
    slots_json = db.Column(JSONB, default=dict)
    context_json = db.Column(JSONB, default=dict)

    updated_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    # relaciones
    usuario = db.relationship("Usuario", back_populates="context")
    # con Cliente basta el backref que ya tienes en Cliente.context
