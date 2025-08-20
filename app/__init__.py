# app/__init__.py
from __future__ import annotations
from flask import Flask, jsonify
from app.config import Config
from app.extensions import db



# 🔹 NUEVO: smorest para OpenAPI/Swagger
from flask_smorest import Api

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.setdefault("JSON_SORT_KEYS", False)

    # 🔹 NUEVO: Config mínima de OpenAPI/Swagger UI
    app.config.setdefault("API_TITLE", "Liora API")
    app.config.setdefault("API_VERSION", "v1")
    app.config.setdefault("OPENAPI_VERSION", "3.0.3")
    app.config.setdefault("OPENAPI_URL_PREFIX", "/docs")   # UI y spec bajo /docs
    app.config.setdefault("OPENAPI_SWAGGER_UI_PATH", "/")
    app.config.setdefault(
        "OPENAPI_SWAGGER_UI_URL",
        "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.10.5/"
    )

    db.init_app(app)

    # 🔹 NUEVO: Instancia de Api (monta /docs y /docs/openapi.json)
    api = Api(app)

    
    # (opcional pero útil) seguridad global multi-tenant por header
    api.spec.components.security_scheme(
        "tenantHeader", {"type": "apiKey", "in": "header", "name": "X-Client-ID"}
    )
    api.spec.options["security"] = [{"tenantHeader": []}]

    @app.get("/health")
    def health():
        return jsonify({"ok": True, "service": "liora-api"}), 200

    _register_blueprints(app, api)  # ← pasa también la instancia Api

    # ⚠️ Solo para entornos efímeros sin Alembic:
    if app.config.get("LIORA_DB_CREATE") == "1":
        with app.app_context():
            from . import models
            db.create_all()

    return app

def _register_blueprints(app: Flask, api: Api) -> None:
    # errores globales se registran en Flask
    try:
        from app.views.errors import errors_bp
        app.register_blueprint(errors_bp)
    except Exception as e:
        app.logger.warning(f"[init] errors_bp no registrado: {e}")

    # 🔹 IMPORTANTE: api_v1 (smorest.Blueprint) se registra en 'api'
    try:
        from app.views.api_view import api_v1
        api.register_blueprint(api_v1)
    except Exception as e:
        app.logger.warning(f"[init] api_v1 no registrado: {e}")
