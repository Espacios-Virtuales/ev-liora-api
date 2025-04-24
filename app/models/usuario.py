from app.extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    membresia_id = db.Column(db.Integer, db.ForeignKey('membresias.id'), nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=True)
    numero_whatsapp_id = db.Column(db.Integer, db.ForeignKey('numeros_whatsapp.id'), nullable=True)

    numero_whatsapp = db.relationship('NumeroWhatsApp', backref='usuarios')

    def __repr__(self):
        return f"<Usuario {self.email}>"