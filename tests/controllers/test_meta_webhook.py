# tests/controllers/test_meta_webhook_flow.py
import os, json, hmac, hashlib
from flask import g

# ---------- Helpers ----------
def _sign(secret: str, body: bytes) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def test_webhook_verify_ok(client, monkeypatch):
    # Config que usa tu controller
    monkeypatch.setenv("WABA_VERIFY_TOKEN", "changeme")

    r = client.get("/api/v1/webhook/meta?hub.mode=subscribe&hub.verify_token=changeme&hub.challenge=123")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "123"


def test_webhook_events_text_ok(client, app, monkeypatch):
    # Entorno que usa el controller
    monkeypatch.setenv("WABA_APP_SECRET", "secret")
    monkeypatch.setenv("META_ACCESS_TOKEN", "mock-token")
    # Fallback de DEMO_CLIENTE_ID si no tienes middleware que setee g.cliente_id
    monkeypatch.setenv("DEMO_CLIENTE_ID", "00000000-0000-0000-0000-000000000000")

    # Mockear router_service y send_text para no tocar integraciones reales
    # handle_incoming debe devolver body para enviar por WhatsApp
    def fake_handle_incoming(evento, estado, deps):
        assert "cliente_id" in estado
        return {"type": "text", "body": "Hola desde Liora"}

    def fake_send_text(to, body, waba_account):
        # Simple verificación de parámetros
        assert to == "56911"
        assert body.startswith("Hola")
        assert "phone_number_id" in waba_account
        return True

    monkeypatch.setattr("app.services.core.router_service.handle_incoming", fake_handle_incoming)
    monkeypatch.setattr("app.services.integrations.whatsapp_service.send_text", fake_send_text)

    # Payload típico de Meta
    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "metadata": {"phone_number_id": "999"},
                    "contacts": [{"wa_id": "56911"}],
                    "messages": [{"from": "56911", "text": {"body": "catalogo"}}]
                }
            }]
        }]
    }
    body = json.dumps(payload).encode()
    sig = _sign("secret", body)

    # Ejecutar POST
    r = client.post(
        "/api/v1/webhook/meta",
        data=body,
        headers={
            "X-Hub-Signature-256": sig,
            "Content-Type": "application/json",
        },
    )
    assert r.status_code == 200
    data = r.get_json()
    assert data.get("ok") is True
