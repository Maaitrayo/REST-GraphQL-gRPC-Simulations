from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from rest.app.db.order_database import get_order_session
from rest.app.db.user_database import get_user_session
from rest.app.repositories.order_repository import OrderRepository
from rest.app.repositories.user_repository import UserRepository
from rest.app.schemas.order import OrderCreate, OrderRead, OrderUpdate
from rest.app.services.order_service import (
    OrderNotFoundError,
    OrderService,
    OrderUserNotFoundError,
)


router = APIRouter(prefix="/orders", tags=["orders"])


def get_order_db_session() -> Generator[Session, None, None]:
    session = get_order_session()
    try:
        yield session
    finally:
        session.close()


def get_user_db_session() -> Generator[Session, None, None]:
    session = get_user_session()
    try:
        yield session
    finally:
        session.close()


def get_order_service(
    order_session: Session = Depends(get_order_db_session),
    user_session: Session = Depends(get_user_db_session),
) -> OrderService:
    order_repository = OrderRepository(order_session)
    user_repository = UserRepository(user_session)
    return OrderService(order_repository, user_repository)


@router.get("", response_model=list[OrderRead])
def list_orders(service: OrderService = Depends(get_order_service)) -> list[OrderRead]:
    return service.list_orders()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, service: OrderService = Depends(get_order_service)) -> OrderRead:
    try:
        return service.get_order(order_id)
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    service: OrderService = Depends(get_order_service),
) -> OrderRead:
    try:
        return service.create_order(payload)
    except OrderUserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{order_id}", response_model=OrderRead)
def update_order(
    order_id: int,
    payload: OrderUpdate,
    service: OrderService = Depends(get_order_service),
) -> OrderRead:
    try:
        return service.update_order(order_id, payload)
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
) -> Response:
    try:
        service.delete_order(order_id)
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
