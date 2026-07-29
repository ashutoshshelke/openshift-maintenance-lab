import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_index(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["service"] == "openshift-maintenance-lab"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_divide(client):
    response = client.get("/divide?a=20&b=4")

    assert response.status_code == 200
    assert response.get_json()["result"] == 5.0


def test_divide_rejects_zero_denominator(client):
    response = client.get("/divide?a=20&b=0")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Denominator cannot be zero"


def test_divide_rejects_invalid_input(client):
    response = client.get("/divide?a=hello&b=4")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Parameters must be valid numbers"


def test_items_uses_requested_limit(client):
    response = client.get("/items?limit=20")

    assert response.status_code == 200
    assert response.get_json()["limit"] == 20


def test_items_rejects_invalid_limit(client):
    response = client.get("/items?limit=invalid")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Limit must be an integer"


def test_items_rejects_out_of_range_limit(client):
    response = client.get("/items?limit=500")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Limit must be between 1 and 100"