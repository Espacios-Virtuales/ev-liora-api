from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Membresia(db.Model):
    __tablename__ = 'membresias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    usuarios = db.relationship('Usuario', backref='membresia', lazy=True)

class Documento(db.Model):
    __tablename__ = 'documentos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    enlace = db.Column(db.String(500), nullable=False)
    usuarios = db.relationship('Usuario', backref='documento', lazy=True)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    membresia_id = db.Column(db.Integer, db.ForeignKey('membresias.id'), nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=True)

    def __repr__(self):
        return f"<Usuario {self.email}>"
