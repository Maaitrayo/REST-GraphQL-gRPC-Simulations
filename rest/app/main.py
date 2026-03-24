from fastapi import FastAPI

from rest.app.api.v1.orders import router as orders_router
from rest.app.api.v1.users import router as users_router
from rest.app.core.config import settings
from rest.app.db.order_database import init_order_database
from rest.app.db.user_database import init_user_database


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.app_version)

    @app.on_event("startup")
    def on_startup() -> None:
        init_user_database()
        init_order_database()

    app.include_router(orders_router, prefix=settings.api_v1_prefix)
    app.include_router(users_router, prefix=settings.api_v1_prefix)

    @app.get(f"{settings.api_v1_prefix}/health", tags=["health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
