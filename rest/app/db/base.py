from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so SQLAlchemy registers them before metadata.create_all() runs.
from rest.app.models.order import Order  # noqa: E402,F401
from rest.app.models.user import User  # noqa: E402,F401
