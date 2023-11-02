"""Order item interface"""

from abc import abstractmethod
from django.db.models import QuerySet

from order_app.models import OrderItem, Order
from cart_app.models import Cart


class IOrderItem:
    """Order item"""

    @abstractmethod
    def get_by_order(self, _order: Order) -> QuerySet[OrderItem]:
        """Получить продкуты по заказу."""
        pass

    @abstractmethod
    def bulk_create(self, _bulk_list: list) -> None:
        """bulk_create для OrderItem"""
        pass
