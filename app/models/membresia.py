from app.extensions import db

class Membresia(db.Model):
    __tablename__ = 'membresias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    usuarios = db.relationship('Usuario', backref='membresia', lazy=True)
