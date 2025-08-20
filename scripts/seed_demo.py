# scripts/seed_demo.py
import uuid
from ../app import create_app
from ../app.extensions import db
from ../app.models.cliente import Cliente

app = create_app()
with app.app_context():
    if not db.session.query(Cliente).filter_by(slug="demo").first():
        demo = Cliente(id=uuid.uuid4(), slug="demo", nombre="Cliente Demo", plan="free")
        db.session.add(demo)
        db.session.commit()
        print("✅ Cliente Demo creado")
    else:
        print("ℹ️ Cliente Demo ya existe")
