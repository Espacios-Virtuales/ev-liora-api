# app/models/convo_state.py
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.extensions import db

class ConvoState(db.Model):
    __tablename__ = 'convo_states'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    waba_account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('waba_accounts.id'), index=True, nullable=True)
    __table_args__ = (
        db.UniqueConstraint("cliente_id","user_msisdn", name="uq_convo_cliente_msisdn"),
    )
    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey('clientes.id'), index=True, nullable=False)
    user_msisdn = db.Column(db.String(32), nullable=False, index=True)  # "5699xxxxxxx"
    last_intent = db.Column(db.String(64))
    slots_json = db.Column(db.JSON)      # {"color": "negro", "talla": "M"}
    context_json = db.Column(db.JSON)    # datos auxiliares, UTM, menú, etc.
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    waba_account = db.relationship('WabaAccount', back_populates='convo_states')
    cliente = db.relationship('Cliente', back_populates='convo_states')

    __table_args__ = (
        db.UniqueConstraint('waba_account_id', 'user_msisdn', name='uq_state_waba_user'),
    )
