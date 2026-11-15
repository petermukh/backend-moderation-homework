import pytest
from fastapi.testclient import TestClient

from main import app
from services import get_prediction_service


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def advertisement():
    return {
        "seller_id": 1,
        "is_verified_seller": False,
        "item_id": 2,
        "name": "Book",
        "description": "Used book",
        "category": 3,
        "images_qty": 0,
    }


@pytest.mark.parametrize(
    ("is_verified_seller", "images_qty", "has_violation"),
    [
        (True, 0, False),
        (True, 2, False),
        (False, 1, False),
        (False, 3, False),
        (False, 0, True),
    ],
)
def test_prediction_results(
    client, advertisement, is_verified_seller, images_qty, has_violation
):
    advertisement.update(
        is_verified_seller=is_verified_seller, images_qty=images_qty
    )

    response = client.post("/predict", json=advertisement)

    assert response.status_code == 200
    assert response.json() is has_violation


@pytest.mark.parametrize(
    "missing_field",
    [
        "seller_id",
        "is_verified_seller",
        "item_id",
        "name",
        "description",
        "category",
        "images_qty",
    ],
)
def test_missing_required_field_returns_400(client, advertisement, missing_field):
    del advertisement[missing_field]

    response = client.post("/predict", json=advertisement)

    assert response.status_code == 400
    assert any(
        missing_field in error["loc"] for error in response.json()["errors"]
    )


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("seller_id", "1"),
        ("is_verified_seller", "true"),
        ("item_id", 1.5),
        ("name", 123),
        ("description", None),
        ("category", True),
        ("images_qty", "2"),
        ("seller_id", 0),
        ("item_id", -1),
        ("name", "  "),
        ("description", "  "),
        ("category", 0),
        ("images_qty", -1),
    ],
)
def test_invalid_value_returns_400(
    client, advertisement, field, invalid_value
):
    advertisement[field] = invalid_value

    response = client.post("/predict", json=advertisement)

    assert response.status_code == 400
    assert any(field in error["loc"] for error in response.json()["errors"])


def test_business_logic_error_returns_500(client, advertisement):
    class BrokenService:
        def predict(self, advertisement):
            raise RuntimeError("private failure detail")

    app.dependency_overrides[get_prediction_service] = lambda: BrokenService()

    response = client.post("/predict", json=advertisement)

    assert response.status_code == 500
    assert response.json() == {"detail": "Prediction failed"}


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
