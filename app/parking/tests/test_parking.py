from fastapi.testclient import TestClient
from app.main import app


def test_parking_spots_endpoint():
    client = TestClient(app)
    r = client.get("/api/parking/spots")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
