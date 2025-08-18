# app/models/usuario.py
from app.extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    membresia_id = db.Column(db.Integer, db.ForeignKey('membresias.id'), nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=True)

    # Multi-tenant: usuario pertenece a un cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True, index=True)

    # Vínculo opcional directo a WABA (si aplica en tu flujo)
    waba_account_id = db.Column(db.Integer, db.ForeignKey('waba_accounts.id'), nullable=True)

    # Relaciones
    documento = db.relationship('Documento', backref='usuarios', lazy=True)

    # 1:1 – cada usuario tiene un solo contexto (scoped por cliente_id)
    context = db.relationship(
        "UserContext",
        backref="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Usuario → Cliente (N:1)
    cliente = db.relationship("Cliente", backref="usuarios", lazy=True)

    def __repr__(self):
        return f"<Usuario {self.email}>"

