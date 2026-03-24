from fastapi import FastAPI

from rest.app.core.config import settings
from rest.app.db.order_database import init_order_database
from rest.app.db.user_database import init_user_database


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.app_version)

    @app.on_event("startup")
    def on_startup() -> None:
        init_user_database()
        init_order_database()

    @app.get(f"{settings.api_v1_prefix}/health", tags=["health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
