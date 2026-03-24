from pathlib import Path

from fastapi.testclient import TestClient

from rest.app.main import app


BASE_DIR = Path(__file__).resolve().parents[1]
USERS_DB_PATH = BASE_DIR / "rest" / "users.db"
ORDERS_DB_PATH = BASE_DIR / "rest" / "orders.db"


def reset_databases() -> None:
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
