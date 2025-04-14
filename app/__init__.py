from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.views.api_view import api_bp
    app.register_blueprint(api_bp)

    return app

from app.models.db_models import db
from app.config import Config

app.config.from_object(Config)
db.init_app(app)

from app.models.db_models import db
from app.config import Config

app.config.from_object(Config)
db.init_app(app)
