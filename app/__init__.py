from flask import Flask
from app.config import Config
from app.extensions import db

from app.views.api_view import api_bp
from app.views.whatsapp_view import whatsapp_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(api_bp)
    app.register_blueprint(whatsapp_bp)
    

    with app.app_context():
        from . import models  # Importa tus modelos aquí
        db.create_all()  # Crea todas las tablas

    return app
