from rest.app.models.user import User
from rest.app.repositories.user_repository import UserRepository
from rest.app.schemas.user import UserCreate, UserUpdate


class UserNotFoundError(Exception):
    pass


class UserEmailAlreadyExistsError(Exception):
    pass


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

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

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.repository.delete(user)
