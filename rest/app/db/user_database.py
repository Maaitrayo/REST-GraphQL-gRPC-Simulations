import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from rest.app.db.base import Base


BASE_DIR = Path(__file__).resolve().parents[2] / "db"
os.makedirs(BASE_DIR, exist_ok=True)
USER_DATABASE_URL = f"sqlite:///{BASE_DIR / 'users.db'}"

user_engine = create_engine(USER_DATABASE_URL, connect_args={"check_same_thread": False})
UserSessionLocal = sessionmaker(bind=user_engine, autoflush=False, autocommit=False)


def init_user_database() -> None:
    Base.metadata.create_all(bind=user_engine)


def get_user_session() -> Session:
    return UserSessionLocal()
