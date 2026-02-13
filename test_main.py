from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    """Проверка endpoint /health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_products():
    """Проверка endpoint /products"""
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_search():
    """проверка поиска по названию"""
    response = client.get("/search?q=5090")
    assert response.status_code == 200
    assert len(response.json()) > 0
