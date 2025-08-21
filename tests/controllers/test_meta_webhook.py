import hmac, hashlib, json

def sign(app_secret: str, body: bytes) -> str:
    return "sha256=" + hmac.new(app_secret.encode(), body, hashlib.sha256).hexdigest()

def test_webhook_verify_get(client):
    resp = client.get("/api/v1/webhook/meta?hub.mode=subscribe&hub.verify_token=changeme&hub.challenge=123")
    assert resp.status_code == 200
    assert resp.data == b"123"

def test_webhook_events_post(client, monkeypatch, app):
    app_secret = "secret"
    event = {"entry":[{"changes":[{"value":{"messages":[{"from":"56911","text":{"body":"catalogo"}}]}}]}]}
    body = json.dumps(event).encode()
    signature = sign(app_secret, body)

    from app.services.core import router_service
    called = {"ok": False}
    def fake_handle(evt, state): called["ok"] = True; return {"ok": True, "text": "ok"}
    monkeypatch.setattr(router_service, "handle_incoming", fake_handle)

    resp = client.post("/api/v1/webhook/meta",
                       data=body,
                       headers={"X-Hub-Signature-256": signature,
                                "Content-Type": "application/json"})
    assert resp.status_code == 200
    assert called["ok"] is True
