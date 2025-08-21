import json, hmac, hashlib

def test_e2e_catalog_publish_and_intent(client, app, monkeypatch):
    csv_data = "sku,name,url\nA1,Polera,https://tienda/polera\n"
    resp = client.post("/api/v1/clientes/00000000-0000-0000-0000-000000000001/catalog/publish",
                       data={"file": (csv_data.encode(), "catalog.csv")},
                       headers={"X-Client-ID": "00000000-0000-0000-0000-000000000001"})
    assert resp.status_code in (200, 201)

    event = {"entry":[{"changes":[{"value":{"messages":[{"from":"56911","text":{"body":"catalogo"}}]}}]}]}
    body = json.dumps(event).encode()
    signature = "sha256=" + hmac.new(b"secret", body, hashlib.sha256).hexdigest()

    from app.services import whatsapp_service
    sent = {"count": 0}
    def fake_send_text(to, body, waba): sent["count"] += 1; return True
    monkeypatch.setattr(whatsapp_service, "send_text", fake_send_text)

    resp2 = client.post("/api/v1/webhook/meta",
                        data=body,
                        headers={"X-Hub-Signature-256": signature,
                                 "Content-Type": "application/json"})
    assert resp2.status_code == 200
    assert sent["count"] >= 1
