# app/models/client_context.py
from app.extensions import db

class ClientContext(db.Model):
    __tablename__ = "client_contexts"

    id = db.Column(db.Integer, primary_key=True)

    # 1:1 con Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False, unique=True, index=True)

    policy_json   = db.Column(db.JSON, default={})   # features, cuotas, planes
    vars_json     = db.Column(db.JSON, default={})   # variables de prompt / plantillas
    channels_json = db.Column(db.JSON, default={})   # waba/ig/webhooks
    meta_json     = db.Column(db.JSON, default={})

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
