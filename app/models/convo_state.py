# app/models/convo_state.py
from app.extensions import db

class ConvoState(db.Model):
    __tablename__ = 'convo_states'

    id = db.Column(db.Integer, primary_key=True)
    waba_account_id = db.Column(db.Integer, db.ForeignKey('waba_accounts.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))  # puede determinarse luego
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
