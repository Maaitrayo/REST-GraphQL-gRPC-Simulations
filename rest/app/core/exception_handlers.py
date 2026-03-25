from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from rest.app.core.exceptions import AppError, ErrorResponse


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        payload = ErrorResponse(detail=exc.detail, error_code=exc.error_code)
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, __: Exception) -> JSONResponse:
        payload = ErrorResponse(
            detail="An unexpected error occurred.",
            error_code="internal_server_error",
        )
        return JSONResponse(status_code=500, content=payload.model_dump())
