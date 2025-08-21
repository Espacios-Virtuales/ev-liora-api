from app.models.cliente import Cliente

def test_cliente_creacion(session):
    c = Cliente(slug="demo", nombre="Cliente Demo", plan="free", estado="activo")
    session.add(c); session.commit()
    assert c.id is not None
    assert c.slug == "demo"
    assert c.created_at is not None and c.updated_at is not None
