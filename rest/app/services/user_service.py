from rest.app.models.order import Order
from rest.app.models.user import User
from rest.app.repositories.order_repository import OrderRepository
from rest.app.repositories.user_repository import UserRepository
from rest.app.schemas.user import UserCreate, UserUpdate


class UserNotFoundError(Exception):
    pass


class UserEmailAlreadyExistsError(Exception):
    pass


class UserHasOrdersError(Exception):
    pass


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
            raise UserNotFoundError(f"User with id {user_id} was not found.")
        return user

    def create_user(self, payload: UserCreate) -> User:
        existing_user = self.repository.get_by_email(str(payload.email))
        if existing_user is not None:
            raise UserEmailAlreadyExistsError(
                f"User with email {payload.email} already exists."
            )

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
                raise UserEmailAlreadyExistsError(
                    f"User with email {new_email} already exists."
                )
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
                raise UserHasOrdersError(
                    f"User with id {user_id} cannot be deleted because orders exist."
                )

        self.repository.delete(user)
