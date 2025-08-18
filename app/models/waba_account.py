# app/models/waba_account.py
from app.extensions import db

class WabaAccount(db.Model):
    __tablename__ = 'waba_accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))  # alias interno (opcional)
    waba_id = db.Column(db.String(100), nullable=False, unique=True, index=True)
    phone_number_id = db.Column(db.String(100), nullable=False, unique=True, index=True)
    numero_e164 = db.Column(db.String(20), nullable=False, unique=True)  # "+1..."
    access_token = db.Column(db.Text, nullable=False)   # mover desde .env → DB (multi-cuenta)
    verify_token = db.Column(db.String(255), nullable=False)
    app_secret = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(20), default='activo')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relaciones
    clientes = db.relationship('Cliente', back_populates='waba_account', cascade='all, delete-orphan')
    convo_states = db.relationship('ConvoState', back_populates='waba_account', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<WabaAccount {self.numero_e164}>"