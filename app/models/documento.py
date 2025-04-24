from app.extensions import db

class Documento(db.Model):
    __tablename__ = 'documentos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    enlace = db.Column(db.String(500), nullable=False)
    usuarios = db.relationship('Usuario', backref='documento', lazy=True)