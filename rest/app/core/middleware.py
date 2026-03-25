import logging
import time

from fastapi import FastAPI, Request


logger = logging.getLogger("rest_api")


def configure_logging() -> None:
    if logger.handlers:
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def register_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def log_and_time_requests(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        logger.info(
            "%s %s -> %s in %.6fs",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )
        return response
