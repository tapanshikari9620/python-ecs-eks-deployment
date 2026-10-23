from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_application_information():
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert data["application"] == "python-demo-app"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_message_endpoint():
    response = client.get("/api/v1/message")

    assert response.status_code == 200
    data = response.json()

    assert data["application"] == "python-demo-app"
    assert data["message"] == "Hello from the Python Demo API!"


def test_info_endpoint():
    response = client.get("/api/v1/info")

    assert response.status_code == 200
    data = response.json()

    assert data["application"] == "python-demo-app"
    assert data["version"] == "1.0.0"
    assert data["python_version"]
    assert data["fastapi_version"]


def test_create_message():
    response = client.post(
        "/api/v1/message",
        json={"message": "Hello AWS"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Hello AWS"
    assert response.json()["length"] == 9


def test_create_message_rejects_empty_message():
    response = client.post(
        "/api/v1/message",
        json={"message": ""},
    )

    assert response.status_code == 422
    assert response.json()["error"] == "Validation failed"


def test_create_message_rejects_missing_message():
    response = client.post(
        "/api/v1/message",
        json={},
    )

    assert response.status_code == 422
