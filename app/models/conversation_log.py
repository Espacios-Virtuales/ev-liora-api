# app/models/conversation_log.py
from app.extensions import db

class ConversationLog(db.Model):
    __tablename__ = 'conversation_logs'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    waba_account_id = db.Column(db.Integer, db.ForeignKey('waba_accounts.id'), nullable=False)
    user_msisdn = db.Column(db.String(32), nullable=False, index=True)
    direction = db.Column(db.String(8), nullable=False)  # "in" | "out"
    intent = db.Column(db.String(64))
    slots_json = db.Column(db.JSON)
    message_type = db.Column(db.String(32))  # "text" | "button" | "media"
    message_body = db.Column(db.Text)
    link_ctrs_json = db.Column(db.JSON)  # {"bitly_url": clicks, ...}
    handoff = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    cliente = db.relationship('Cliente', back_populates='conversation_logs')
