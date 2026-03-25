from sqlalchemy import select
from sqlalchemy.orm import Session

from rest.app.models.order import Order


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_orders(
        self,
        *,
        offset: int = 0,
        limit: int | None = None,
        user_id: int | None = None,
        status: str | None = None,
    ) -> list[Order]:
        statement = select(Order).order_by(Order.id)
        if user_id is not None:
            statement = statement.where(Order.user_id == user_id)
        if status is not None:
            statement = statement.where(Order.status == status)

        statement = statement.offset(offset)
        if limit is not None:
            statement = statement.limit(limit)
        return list(self.session.scalars(statement).all())

    def get_by_id(self, order_id: int) -> Order | None:
        return self.session.get(Order, order_id)

    def list_by_user_id(self, user_id: int) -> list[Order]:
        statement = select(Order).where(Order.user_id == user_id).order_by(Order.id)
        return list(self.session.scalars(statement).all())

    def create(self, *, user_id: int, product_name: str, quantity: int) -> Order:
        order = Order(user_id=user_id, product_name=product_name, quantity=quantity)
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def update(self, order: Order, **changes: object) -> Order:
        for field, value in changes.items():
            setattr(order, field, value)

        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def delete(self, order: Order) -> None:
        self.session.delete(order)
        self.session.commit()
