from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    user_id: int
    product_name: str = Field(..., min_length=1, max_length=255)
    quantity: int = Field(default=1, ge=1)


class OrderUpdate(BaseModel):
    product_name: str | None = Field(default=None, min_length=1, max_length=255)
    quantity: int | None = Field(default=None, ge=1)
    status: str | None = Field(default=None, min_length=1, max_length=50)


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    product_name: str
    quantity: int
    status: str
    created_at: datetime
