from app.src.app import app

def test_health_endpoint():
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json == {"status": "ok"}

def test_get_users_endpoint():
    client = app.test_client()
    r = client.get("/users")
    assert r.status_code == 200
    assert isinstance(r.json, list)
