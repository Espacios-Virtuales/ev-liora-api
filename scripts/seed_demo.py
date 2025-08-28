# scripts/seed_demo.py
import uuid
from app import create_app
from app.extensions import db
from app.models.cliente import Cliente

def seed_cliente(slug="demo"):
    c = Cliente(id=uuid.uuid4(), nombre="Demo", slug=slug)
    db.session.add(c)
    db.session.commit()
    return c

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        cliente = seed_cliente()
        print("Cliente demo creado:", cliente.id, cliente.slug)
