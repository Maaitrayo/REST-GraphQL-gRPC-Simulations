from sqlalchemy import select
from sqlalchemy.orm import Session

from rest.app.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_users(self) -> list[User]:
        statement = select(User).order_by(User.id)
        return list(self.session.scalars(statement).all())

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.session.scalars(statement).first()

    def create(self, *, name: str, email: str, is_active: bool) -> User:
        user = User(name=name, email=email, is_active=is_active)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User, **changes: object) -> User:
        for field, value in changes.items():
            setattr(user, field, value)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
