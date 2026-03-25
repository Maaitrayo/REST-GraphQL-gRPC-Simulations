from rest.app.core.exceptions import AppError
from rest.app.models.order import Order
from rest.app.repositories.order_repository import OrderRepository
from rest.app.repositories.user_repository import UserRepository
from rest.app.schemas.order import OrderCreate, OrderUpdate


class OrderNotFoundError(AppError):
    def __init__(self, order_id: int) -> None:
        super().__init__(
            detail=f"Order with id {order_id} was not found.",
            error_code="order_not_found",
            status_code=404,
        )


class OrderUserNotFoundError(AppError):
    def __init__(self, user_id: int) -> None:
        super().__init__(
            detail=f"User with id {user_id} was not found.",
            error_code="order_user_not_found",
            status_code=400,
        )


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
    ) -> None:
        self.order_repository = order_repository
        self.user_repository = user_repository

    def list_orders(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        user_id: int | None = None,
        status: str | None = None,
    ) -> list[Order]:
        offset = (page - 1) * limit
        return self.order_repository.list_orders(
            offset=offset,
            limit=limit,
            user_id=user_id,
            status=status,
        )

    def get_order(self, order_id: int) -> Order:
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order

    def create_order(self, payload: OrderCreate) -> Order:
        user = self.user_repository.get_by_id(payload.user_id)
        if user is None:
            raise OrderUserNotFoundError(payload.user_id)

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
