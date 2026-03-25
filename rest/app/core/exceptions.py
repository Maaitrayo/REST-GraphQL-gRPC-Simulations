from dataclasses import dataclass

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str
    error_code: str


@dataclass
class AppError(Exception):
    detail: str
    error_code: str
    status_code: int
