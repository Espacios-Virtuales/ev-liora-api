from app.extensions import db

class NumeroWhatsApp(db.Model):
    __tablename__ = 'numeros_whatsapp'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False, unique=True)
    waba_id = db.Column(db.String(100), nullable=False)
    phone_number_id = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    webhook_url = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.String(20), default='activo')

    def __repr__(self):
        return f"<NumeroWhatsApp {self.numero}>"
