from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.views.whatsapp_view import whatsapp_bp
    app.register_blueprint(whatsapp_bp)

    return app
