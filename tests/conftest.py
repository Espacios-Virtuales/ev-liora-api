import os, sys, pytest, pathlib

# Asegura que el repo root esté en sys.path (tests/ está a 1 nivel)
REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Intenta importar create_app desde app.__init__ o desde main.py como fallback
try:
    from app import create_app
except Exception:
    from main import create_app

try:
    from app.extensions import db
except Exception as e:
    # Si falla, da un mensaje claro
    raise ImportError("No se pudo importar app.extensions.db. "
                      "Verifica que 'app/extensions.py' exista y exporte 'db'.") from e

@pytest.fixture(scope="session")
def app():
    os.environ.setdefault("FLASK_ENV", "testing")
    cfg = {
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "TESTING": True,
        "PROPAGATE_EXCEPTIONS": True,
    }
    app = create_app(cfg)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def session(app):
    with app.app_context():
        yield db.session
