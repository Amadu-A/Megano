"""Репозитарий Order"""
from typing import Optional
from beartype import beartype
from django.db.models import QuerySet

from interface.order_interface import IOrder
from order_app.models import Order
from auth_app.models import User


class OrderRepository(IOrder):

    @beartype
    def save(self, model: Order) -> None:
        model.save()

    @beartype
    def get_list_by_user(self, _user: User) -> QuerySet[Order]:
        """Получить список заказов пользоветеля."""

        return Order.objects.filter(user=_user).order_by('-created_at')

    @beartype
    def get_last_by_user(self, _user: User) -> Optional[Order]:
        """Получить последний заказ покупателя по дате создания"""

        try:
            return Order.objects.filter(user=_user).latest('created_at')
        except Order.DoesNotExist:
            return None

    @beartype
    def get_by_pk(self, _pk: int) -> Optional[Order]:
        """Получить заказ по pk"""
        try:
            return Order.objects.get(pk=_pk)
        except Order.DoesNotExist:
            return None

    @beartype
    def get_by_payment_id(self, _payment_id: str) -> Optional[Order]:
        """Получить заказ по идентификатору оплаты"""
        try:
            return Order.objects.get(payment_id=_payment_id)
        except Order.DoesNotExist:
            return None
