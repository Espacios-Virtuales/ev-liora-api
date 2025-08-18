# app/models/user_context.py
from app.extensions import db

class UserContext(db.Model):
    __tablename__ = "user_contexts"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False, index=True)

    msisdn = db.Column(db.String(30))
    last_intent = db.Column(db.String(50))
    slots_json = db.Column(db.JSON, default={})
    context_json = db.Column(db.JSON, default={})
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # (opcional, al final del archivo)
    #  db.Index("ix_user_contexts_cliente_usuario", UserContext.cliente_id, UserContext.usuario_id)
