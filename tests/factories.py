# tests/factories.py (o tu helper)
import uuid
from app.extensions import db
from app.models.cliente import Cliente

def seed_cliente(app, slug=None) -> Cliente:
    """Crea y devuelve el objeto Cliente (con expire_on_commit=False no se expira)."""
    with app.app_context():
        c = Cliente(id=uuid.uuid4(), nombre="Demo", slug=slug or f"demo-{uuid.uuid4().hex[:8]}")
        db.session.add(c); db.session.commit()
        return c
