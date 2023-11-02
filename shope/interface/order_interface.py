from abc import abstractmethod
from typing import Optional
from django.db.models import QuerySet

from order_app.models import Order
from auth_app.models import User


class IOrder:

    @abstractmethod
    def save(self, model: Order) -> None:
        """Сохранить заказ."""
        pass

    @abstractmethod
    def get_list_by_user(self, _user: User) -> QuerySet[Order]:
        """Получить список заказов пользоветеля."""
        pass

    @abstractmethod
    def get_last_by_user(self, _user: User) -> Optional[Order]:
        """Получить последний заказ покупателя по дате создания"""
        pass

    @abstractmethod
    def get_by_pk(self, _pk: int) -> Optional[Order]:
        """Получить заказ по pk"""
        pass

    @abstractmethod
    def get_by_payment_id(self, _payment_id: str) -> Optional[Order]:
        """Получить заказ по идентификатору оплаты"""
        pass
