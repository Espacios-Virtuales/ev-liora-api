# tests/models/test_cliente_step1.py
import pytest
from sqlalchemy.exc import IntegrityError
from app.models.cliente import Cliente

# ---------- Helpers ----------
def make_cliente(slug="demo", nombre="Cliente Demo", **extra):
    return Cliente(slug=slug, nombre=nombre, **extra)


def test_cliente_slug_unico(session):
    c1 = make_cliente(slug="andina")
    c2 = make_cliente(slug="andina", nombre="Otro Nombre")
    session.add(c1)
    session.commit()
    session.add(c2)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

def test_cliente_estado_settable(session):
    c = make_cliente(slug="beta", estado="suspendido")
    session.add(c)
    session.commit()
    assert c.estado == "suspendido"

def test_cliente_sheet_campos_opcionales(session):
    c = make_cliente(slug="con-sheet", sheet_id="1AbC", sheet_range="Hoja1!A1:C100")
    session.add(c)
    session.commit()
    assert c.sheet_id == "1AbC"
    assert c.sheet_range == "Hoja1!A1:C100"

# ---------- (Opcional) relaciones si existen, pero sin romper si aún no están ----------
def test_cliente_relaciones_presencia_atributos():
    """
    Validamos que los atributos de relación existan en el modelo,
    pero no exigen que los modelos/relaciones estén operativas aún.
    Útil para mantener el contrato del modelo.
    """
    # No toca la DB — solo inspección de atributos
    c = Cliente(slug="x", nombre="x")
    # Estas relaciones están declaradas en tu clase; si cambian más adelante, ajusta aquí.
    assert hasattr(c, "waba_account")
    assert hasattr(c, "catalog_active")
    assert hasattr(c, "snapshots")
    assert hasattr(c, "ingest_logs")
    assert hasattr(c, "convo_states")
    assert hasattr(c, "conversation_logs")
    assert hasattr(c, "context")
