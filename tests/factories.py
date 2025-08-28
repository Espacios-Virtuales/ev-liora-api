# tests/factories.py
import uuid
from app.extensions import db
from app.models.cliente import Cliente

def seed_cliente(app, slug=None):
    with app.app_context():
        unique = uuid.uuid4().hex[:8]
        c = Cliente(id=uuid.uuid4(), nombre="Demo", slug=slug or f"demo-{unique}")
        db.session.add(c); db.session.commit()
        return c

