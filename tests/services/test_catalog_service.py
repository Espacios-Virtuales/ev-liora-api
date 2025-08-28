# tests/services/test_catalog_service_flow.py
import uuid
import pytest
from flask import g

from app.extensions import db
from app.models.cliente import Cliente
from app.models.catalog_active import CatalogActive
from app.models.catalog_snapshot import CatalogSnapshot
from tests.factories import seed_cliente



from app.services.catalog_service import (
    publish_snapshot,
    activate_snapshot,
    get_active,
    get_active_summary,
    search_active,
)

# ---------- Helpers ----------
VALID_ROWS = [
    {"sku": "A1", "name": "Polera Andina", "url": "https://tienda/polera-andina", "price": 12990},
    {"sku": "A2", "name": "Polera Puna",   "url": "https://tienda/polera-puna",   "price": 13990},
    {"sku": "B1", "name": "Gorro Altiplano","url": "https://tienda/gorro-altiplano"},
]

INVALID_ROWS = [
    {"name": "Sin SKU", "url": "https://x"},        # falta sku
    {"sku": "X1", "url": "https://y"},             # falta name
    {"sku": "X2", "name": "Sin URL"},              # falta url
]


def _seed_cliente(app):
    return seed_cliente(app)  # ya trae slug único

# ---------- Tests ----------
def test_publish_activate_and_summary(app):
    cliente_id = _seed_cliente(app) 

    with app.test_request_context("/"):
        g.cliente_id = cliente_id

        # 1) Publicar snapshot
        snap = publish_snapshot(rows=VALID_ROWS, source="test")
        assert isinstance(snap, CatalogSnapshot)
        assert snap.rows_count == len(VALID_ROWS)
        assert snap.version >= 1
        assert (snap.payload_json or {}).get("rows")

        # 2) Activar snapshot (última versión por defecto)
        active = activate_snapshot()
        assert isinstance(active, CatalogActive)
        assert active.version == snap.version
        assert active.rows_count == snap.rows_count

        # 3) get_active y summary
        current = get_active()
        assert current is not None and current.version == snap.version

        summary = get_active_summary(limit=2)
        assert len(summary) == 2
        assert summary[0]["name"] == "Polera Andina"

        # 4) search_active (por nombre y SKU)
        res_name = search_active(cliente_id=None, q="puna", limit=5)
        assert len(res_name) == 1 and res_name[0]["sku"] == "A2"

        res_sku  = search_active(cliente_id=None, q="B1", limit=5)
        assert len(res_sku) == 1 and res_sku[0]["name"] == "Gorro Altiplano"


def test_publish_snapshot_invalid_rows_raises(app):
    c = _seed_cliente(app)
    with app.test_request_context("/"):
        g.cliente_id = c.id

        # Debe lanzar ValueError si faltan columnas requeridas
        with pytest.raises(ValueError):
            publish_snapshot(rows=INVALID_ROWS, source="test")
