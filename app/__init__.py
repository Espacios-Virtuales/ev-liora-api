from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

from app.views.api_view import api_bp
from app.views.whatsapp_view import whatsapp_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(api_bp)
    app.register_blueprint(whatsapp_bp)
    
    return app
