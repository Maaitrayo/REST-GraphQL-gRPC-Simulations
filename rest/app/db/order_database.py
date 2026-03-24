import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from rest.app.db.base import Base


BASE_DIR = Path(__file__).resolve().parents[2] / "db"
os.makedirs(BASE_DIR, exist_ok=True)
ORDER_DATABASE_URL = f"sqlite:///{BASE_DIR / 'orders.db'}"

order_engine = create_engine(
    ORDER_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
OrderSessionLocal = sessionmaker(bind=order_engine, autoflush=False, autocommit=False)


def init_order_database() -> None:
    Base.metadata.create_all(bind=order_engine)


def get_order_session() -> Session:
    return OrderSessionLocal()
