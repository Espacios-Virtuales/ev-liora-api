import hashlib
from app.services.catalog_service import publish_snapshot, activate
from app.models.catalog_snapshot import CatalogSnapshot
from app.models.catalog_active import CatalogActive

def fake_checksum(rows: bytes) -> str:
    return hashlib.sha256(rows).hexdigest()

def test_publish_and_activate_catalog(session, monkeypatch):
    from app.services import bitly_service
    monkeypatch.setattr(bitly_service, "shorten", lambda url, utm=None: f"https://bit.ly/mock?u={url}")

    csv_bytes = b"sku,name,url\nA1,Polera,https://tienda/polera\n"

    snap = publish_snapshot(cliente_id="00000000-0000-0000-0000-000000000001",
                            csv_bytes=csv_bytes,
                            source="manual")

    assert isinstance(snap, CatalogSnapshot)
    assert snap.checksum == fake_checksum(csv_bytes)

    active = activate(cliente_id=snap.cliente_id, version=snap.version)
    assert isinstance(active, CatalogActive)
    assert active.version == snap.version
