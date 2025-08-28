import os, sys, pytest, pathlib

from sqlalchemy.dialects.postgresql import JSONB as PGJSONB, UUID as PGUUID
from sqlalchemy.ext.compiler import compiles
import types, sys


@compiles(PGJSONB, "sqlite")
def _compile_jsonb_sqlite(element, compiler, **kw):
    return "JSON"

@compiles(PGUUID, "sqlite")
def _compile_uuid_sqlite(element, compiler, **kw):
    return "CHAR(36)"

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
        "SQLALCHEMY_SESSION_OPTIONS": {"expire_on_commit": False},
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


# ---- Shims para plugins requeridos por el router (solo en tests) ----
def _mk_plugin_module(mod_path: str):
    # Derivamos un nombre legible del modulo, p.ej. "ecommerce" desde "app.plugins.ecommerce.plugin"
    parts = mod_path.split(".")
    plugin_name = parts[-2] if len(parts) >= 2 else "plugin"

    class _P:
        supported = {"catalogo.ver", "catalogo.buscar", "vida_sana.menu", "reciclaje.menu"}
        # manifest opcional, por si el registry lo usa
        manifest = types.SimpleNamespace(intents=list(supported))

        def handle(self, intent, message, ctx, deps):
            if intent == "catalogo.buscar":
                q = (message or "").split(" ", 1)[-1] if " " in (message or "") else ""
                return {"type": "text", "body": f"Resultados para: {q or '—'}"}
            if intent == "catalogo.ver":
                return {"type": "text", "body": "Catálogo disponible."}
            if intent.endswith(".menu"):
                return {"type": "text", "body": f"Menú {intent.split('.')[0]}."}
            return {"type": "text", "body": "No match."}

    inst = _P()
    # Asignamos el nombre tanto a la instancia como a la clase (algunos registries leen uno u otro)
    inst.name = plugin_name
    _P.name = plugin_name

    mod = types.ModuleType(mod_path)
    # Cubrimos las 3 variantes comunes que suelen buscar los registries
    mod.plugin = inst                 # atributo 'plugin'
    mod.Plugin = lambda: _P()         # fábrica/clase 'Plugin'
    mod.get_plugin = lambda: inst     # función 'get_plugin()'
    return mod

for path in [
    "app.plugins.ecommerce.plugin",
    "app.plugins.vida_sana.plugin",
    "app.plugins.reciclaje.plugin",
]:
    sys.modules.setdefault(path, _mk_plugin_module(path))
# ---------------------------------------------------------------------
