# app/__init__.py
from __future__ import annotations
from flask import Flask, jsonify
from app.config import Config
from app.extensions import db

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.setdefault("JSON_SORT_KEYS", False)

    db.init_app(app)

    @app.get("/health")
    def health():
        return jsonify({"ok": True, "service": "liora-api"}), 200

    _register_blueprints(app)

    # ⚠️ Solo para entornos efímeros sin Alembic:
    if app.config.get("LIORA_DB_CREATE") == "1":
        with app.app_context():
            from . import models
            db.create_all()

    return app

def _register_blueprints(app: Flask) -> None:
    try:
        from app.views.errors import errors_bp
        app.register_blueprint(errors_bp)
    except Exception as e:
        app.logger.warning(f"[init] errors_bp no registrado: {e}")

    try:
        from app.views.api_view import api_v1
        app.register_blueprint(api_v1)
    except Exception as e:
        app.logger.warning(f"[init] api_v1 no registrado: {e}")
