def test_envelope_success(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert "data" in data

def test_envelope_error(client):
    resp = client.post("/api/v1/clientes", json={})
    assert resp.status_code in (400, 422)
    err = resp.get_json()
    assert err["ok"] is False
    assert "error" in err and "message" in err["error"]
