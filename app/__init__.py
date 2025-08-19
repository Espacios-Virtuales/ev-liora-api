    from flask import Flask, jsonify
    from app.config import Config
    from app.extensions import db

    # Blueprints
    from app.views.api_view import api_v1            # ← nueva API versionada
    from app.views.errors import errors_bp           # ← manejador global de errores

    # (Opcional) si aún usas el blueprint antiguo de WhatsApp:
    # from app.views.whatsapp_view import whatsapp_bp

    def create_app():
        app = Flask(__name__)
        app.config.from_object(Config)

        # Config JSON (mejor DX)
        app.config.setdefault("JSON_SORT_KEYS", False)

        # inicializar extensiones
        db.init_app(app)

        # healthcheck mínimo
        @app.get("/health")
        def health():
            return jsonify({"ok": True, "service": "liora-api"}), 200

        # registrar blueprints (orden: errores primero para capturar todo)
        app.register_blueprint(errors_bp)
        app.register_blueprint(api_v1)
        # (Opcional) app.register_blueprint(whatsapp_bp)

        # MODE DEV: crear tablas si aún no has migrado a Alembic
        with app.app_context():
            from . import models  # asegura que se importen todos los modelos
            db.create_all()       # TODO: remover cuando uses `alembic upgrade head`

        return app
