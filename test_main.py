from fastapi.testclient import TestClient
from main import app, CART, ORDERS

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


def test_get_cart_with_items():
    response = client.get("/cart")
    assert response.status_code == 200
    assert "items" in response.json()
    assert "total" in response.json()


def test_get_cart_empty():
    CART.clear()
    response = client.get("/cart")
    assert response.status_code == 200
    assert response.json() == []


def test_add_cart_valid():
    CART.clear()
    response = client.post("/cart/add?pid=0&qty=2")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert len(CART) == 1


def test_add_cart_invalid_pid():
    response = client.post("/cart/add?pid=999")
    assert response.status_code == 404


def test_clear_cart():
    response = client.delete("/cart")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert len(CART) == 0


def test_checkout_success():
    CART.clear()
    client.post("/cart/add?pid=0&qty=1")
    response = client.post("/checkout")
    assert response.status_code == 200
    assert "items" in response.json()
    assert "total" in response.json()
    assert "created_at" in response.json()
    assert len(CART) == 0


def test_checkout_empty_cart():
    CART.clear()
    response = client.post("/checkout")
    assert response.status_code == 400


def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
