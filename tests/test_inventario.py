from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_list():
    r = client.post("/inventario/", json={"nombre":"Test Producto", "cantidad":5})
    assert r.status_code == 200
    data = r.json()
    assert data["nombre"] == "Test Producto"

    r2 = client.get("/inventario/")
    assert r2.status_code == 200
    items = r2.json()
    assert any(x["nombre"] == "Test Producto" for x in items) 
