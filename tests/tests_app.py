from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_create_page():

    response = client.get(
        "/create"
    )

    assert response.status_code == 200

    assert "ComicCraft" in response.text