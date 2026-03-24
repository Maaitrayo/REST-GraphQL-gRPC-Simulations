from rest.app.models.order import Order
from rest.app.repositories.order_repository import OrderRepository
from rest.app.repositories.user_repository import UserRepository
from rest.app.schemas.order import OrderCreate, OrderUpdate


class OrderNotFoundError(Exception):
    pass


class OrderUserNotFoundError(Exception):
    pass


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
    ) -> None:
        self.order_repository = order_repository
        self.user_repository = user_repository

    def list_orders(self) -> list[Order]:
        return self.order_repository.list_orders()

    def get_order(self, order_id: int) -> Order:
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} was not found.")
        return order

    def create_order(self, payload: OrderCreate) -> Order:
        user = self.user_repository.get_by_id(payload.user_id)
        if user is None:
            raise OrderUserNotFoundError(
                f"User with id {payload.user_id} was not found."
            )

        return self.order_repository.create(
            user_id=payload.user_id,
            product_name=payload.product_name,
            quantity=payload.quantity,
        )

    def update_order(self, order_id: int, payload: OrderUpdate) -> Order:
        order = self.get_order(order_id)
        changes = payload.model_dump(exclude_unset=True)
        return self.order_repository.update(order, **changes)

    def delete_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        self.order_repository.delete(order)
