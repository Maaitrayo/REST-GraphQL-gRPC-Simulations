from rest.app.core.exceptions import AppError
from rest.app.models.order import Order
from rest.app.models.user import User
from rest.app.repositories.order_repository import OrderRepository
from rest.app.repositories.user_repository import UserRepository
from rest.app.schemas.user import UserCreate, UserUpdate


class UserNotFoundError(AppError):
    def __init__(self, user_id: int) -> None:
        super().__init__(
            detail=f"User with id {user_id} was not found.",
            error_code="user_not_found",
            status_code=404,
        )


class UserEmailAlreadyExistsError(AppError):
    def __init__(self, email: str) -> None:
        super().__init__(
            detail=f"User with email {email} already exists.",
            error_code="user_email_already_exists",
            status_code=400,
        )


class UserHasOrdersError(AppError):
    def __init__(self, user_id: int) -> None:
        super().__init__(
            detail=f"User with id {user_id} cannot be deleted because orders exist.",
            error_code="user_has_orders",
            status_code=400,
        )


class UserService:
    def __init__(
        self,
        repository: UserRepository,
        order_repository: OrderRepository | None = None,
    ) -> None:
        self.repository = repository
        self.order_repository = order_repository

    def list_users(self) -> list[User]:
        return self.repository.list_users()

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    def create_user(self, payload: UserCreate) -> User:
        existing_user = self.repository.get_by_email(str(payload.email))
        if existing_user is not None:
            raise UserEmailAlreadyExistsError(str(payload.email))

        return self.repository.create(
            name=payload.name,
            email=str(payload.email),
            is_active=payload.is_active,
        )

    def update_user(self, user_id: int, payload: UserUpdate) -> User:
        user = self.get_user(user_id)
        changes = payload.model_dump(exclude_unset=True)

        new_email = changes.get("email")
        if new_email is not None:
            existing_user = self.repository.get_by_email(str(new_email))
            if existing_user is not None and existing_user.id != user.id:
                raise UserEmailAlreadyExistsError(str(new_email))
            changes["email"] = str(new_email)

        return self.repository.update(user, **changes)

    def get_user_orders(self, user_id: int) -> list[Order]:
        user = self.get_user(user_id)
        if self.order_repository is None:
            raise RuntimeError("Order repository is required for user order queries.")

        return self.order_repository.list_by_user_id(user.id)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)

        if self.order_repository is not None:
            user_orders = self.order_repository.list_by_user_id(user.id)
            if user_orders:
                raise UserHasOrdersError(user_id)

        self.repository.delete(user)
