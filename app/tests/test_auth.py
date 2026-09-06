import os
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.mark.skipif(
    not os.getenv("INITIAL_ADMIN_USERNAME") or not os.getenv("INITIAL_ADMIN_PASSWORD"),
    reason="Auth env vars not set",
)
def test_login_and_me():
    client = TestClient(app)
    username = os.getenv("INITIAL_ADMIN_USERNAME")
    password = os.getenv("INITIAL_ADMIN_PASSWORD")

    # Login
    r = client.post(
        "/api/auth/login", json={"username": username, "password": password}
    )
    assert r.status_code == 200, f"Login failed: {r.status_code} - {r.text}"
    data = r.json()
    assert "access_token" in data
    token = data["access_token"]

    # Get profile
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/api/auth/me", headers=headers)
    assert r.status_code == 200, f"/me failed: {r.status_code} - {r.text}"
    me = r.json()
    assert me.get("username") == username
