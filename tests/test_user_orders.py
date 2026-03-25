"""
Tests for user orders functionality in the REST API.
usuage:
    uv run -m pytest tests/test_user_orders.py
"""

from pathlib import Path

from fastapi.testclient import TestClient

from rest.app.db.order_database import order_engine
from rest.app.db.user_database import user_engine
from rest.app.main import app


BASE_DIR = Path(__file__).resolve().parents[1]
USERS_DB_PATH = BASE_DIR / "rest" / "db" / "users.db"
ORDERS_DB_PATH = BASE_DIR / "rest" / "db" / "orders.db"


def reset_databases() -> None:
    user_engine.dispose()
    order_engine.dispose()
    USERS_DB_PATH.unlink(missing_ok=True)
    ORDERS_DB_PATH.unlink(missing_ok=True)


def test_get_user_orders_returns_orders_for_user() -> None:
    reset_databases()

    with TestClient(app) as client:
        user_response = client.post(
            "/api/v1/users",
            json={
                "name": "Alice",
                "email": "alice@example.com",
                "is_active": True,
            },
        )
        assert user_response.status_code == 201
        user_id = user_response.json()["id"]

        order_response = client.post(
            "/api/v1/orders",
            json={
                "user_id": user_id,
                "product_name": "Laptop",
                "quantity": 1,
            },
        )
        assert order_response.status_code == 201

        user_orders_response = client.get(f"/api/v1/users/{user_id}/orders")

        assert user_orders_response.status_code == 200
        orders = user_orders_response.json()
        assert len(orders) == 1
        assert orders[0]["user_id"] == user_id
        assert orders[0]["product_name"] == "Laptop"
        assert orders[0]["quantity"] == 1


def test_delete_user_with_orders_returns_400() -> None:
    reset_databases()

    with TestClient(app) as client:
        user_response = client.post(
            "/api/v1/users",
            json={
                "name": "Bob",
                "email": "bob@example.com",
                "is_active": True,
            },
        )
        assert user_response.status_code == 201
        user_id = user_response.json()["id"]

        order_response = client.post(
            "/api/v1/orders",
            json={
                "user_id": user_id,
                "product_name": "Keyboard",
                "quantity": 2,
            },
        )
        assert order_response.status_code == 201

        delete_response = client.delete(f"/api/v1/users/{user_id}")

        assert delete_response.status_code == 400
        assert delete_response.json() == {
            "detail": f"User with id {user_id} cannot be deleted because orders exist.",
            "error_code": "user_has_orders",
        }
