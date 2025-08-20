# app/models/waba_account.py
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class WabaAccount(db.Model):
    __tablename__ = 'waba_accounts'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    cliente_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('clientes.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,  
        index=True
    )
    name = db.Column(db.String(120))
    waba_id = db.Column(db.String(100), nullable=False, unique=True, index=True)
    phone_number_id = db.Column(db.String(100), nullable=False, unique=True, index=True)
    numero_e164 = db.Column(db.String(20), nullable=False, unique=True)
    access_token = db.Column(db.Text, nullable=False)
    verify_token = db.Column(db.String(255), nullable=False)
    app_secret = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(20), default='activo')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # relación 1:1 (lado hijo)
    cliente = db.relationship('Cliente', back_populates='waba_account')

    # relaciones existentes
    convo_states = db.relationship(
        'ConvoState',
        back_populates='waba_account',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<WabaAccount {self.numero_e164}>"
