"""
Tests for the users API endpoints.
Usuage:
uv run python -m pytest tests/test_users.py
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


def test_create_and_get_user() -> None:
    reset_databases()

    with TestClient(app) as client:
        create_response = client.post(
            "/api/v1/users",
            json={
                "name": "Alice",
                "email": "alice@example.com",
                "is_active": True,
            },
        )

        assert create_response.status_code == 201
        created_user = create_response.json()
        assert created_user["name"] == "Alice"
        assert created_user["email"] == "alice@example.com"
        assert created_user["is_active"] is True
        assert "id" in created_user

        user_id = created_user["id"]
        get_response = client.get(f"/api/v1/users/{user_id}")

        assert get_response.status_code == 200
        fetched_user = get_response.json()
        assert fetched_user["id"] == user_id
        assert fetched_user["name"] == "Alice"
        assert fetched_user["email"] == "alice@example.com"


def test_create_user_with_duplicate_email_returns_400() -> None:
    reset_databases()

    with TestClient(app) as client:
        first_response = client.post(
            "/api/v1/users",
            json={
                "name": "Alice",
                "email": "alice@example.com",
                "is_active": True,
            },
        )
        assert first_response.status_code == 201

        duplicate_response = client.post(
            "/api/v1/users",
            json={
                "name": "Alice Clone",
                "email": "alice@example.com",
                "is_active": True,
            },
        )

        assert duplicate_response.status_code == 400
        assert duplicate_response.json() == {
            "detail": "User with email alice@example.com already exists.",
            "error_code": "user_email_already_exists",
        }


def test_get_missing_user_returns_404() -> None:
    reset_databases()

    with TestClient(app) as client:
        response = client.get("/api/v1/users/999")

        assert response.status_code == 404
        assert response.json() == {
            "detail": "User with id 999 was not found.",
            "error_code": "user_not_found",
        }
