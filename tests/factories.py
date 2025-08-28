# tests/factories.py
import uuid
from app.extensions import db
from app.models.cliente import Cliente

def seed_cliente(app) -> str:
    with app.app_context():
        c = Cliente(id=uuid.uuid4(), nombre="Demo", slug=f"demo-{uuid.uuid4().hex[:8]}")
        db.session.add(c)
        db.session.commit()
        return str(c.id)  # DEVUELVE EL ID, NO LA INSTANCIA
