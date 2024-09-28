from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"username": "john", "email": "john@example.com", "is_active": True})
    assert response.status_code == 200
    assert response.json()["username"] == "john"

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "john"

def test_update_user():
    response = client.put("/users/1", json={"username": "john_updated"})
    assert response.status_code == 200
    assert response.json()["username"] == "john_updated"

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["ok"] == True
