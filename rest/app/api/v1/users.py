from collections.abc import Generator

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from rest.app.db.order_database import get_order_session
from rest.app.db.user_database import get_user_session
from rest.app.repositories.order_repository import OrderRepository
from rest.app.repositories.user_repository import UserRepository
from rest.app.schemas.order import OrderRead
from rest.app.schemas.user import UserCreate, UserRead, UserUpdate
from rest.app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


def get_db_session() -> Generator[Session, None, None]:
    session = get_user_session()
    try:
        yield session
    finally:
        session.close()


def get_order_db_session() -> Generator[Session, None, None]:
    session = get_order_session()
    try:
        yield session
    finally:
        session.close()


def get_user_service(
    session: Session = Depends(get_db_session),
    order_session: Session = Depends(get_order_db_session),
) -> UserService:
    repository = UserRepository(session)
    order_repository = OrderRepository(order_session)
    return UserService(repository, order_repository)


@router.get("", response_model=list[UserRead])
def list_users(service: UserService = Depends(get_user_service)) -> list[UserRead]:
    return service.list_users()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)) -> UserRead:
    return service.get_user(user_id)


@router.get("/{user_id}/orders", response_model=list[OrderRead])
def get_user_orders(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> list[OrderRead]:
    return service.get_user_orders(user_id)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserRead:
    return service.create_user(payload)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserRead:
    return service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> Response:
    service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
