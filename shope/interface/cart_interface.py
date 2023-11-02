"""Интерфейсы для модели Cart"""
from abc import abstractmethod
from decimal import Decimal
from typing import Optional
from auth_app.models import User
from cart_app.models import Cart


class ICart:
    """ICart"""

    @abstractmethod
    def get_active_by_user(self, _user: User) -> Optional[Cart]:
        """Получить активную корзину пользоветеля."""
        pass

    @abstractmethod
    def save(self, model: Cart) -> None:
        """ Сохранить корзину."""
        pass

    @abstractmethod
    def total_amount(self, model: Cart) -> Optional[Decimal]:
        """ Получить сумму товаров в корзине."""
        pass

    @abstractmethod
    def model_to_list(self, model: Cart) -> Optional[list]:
        """ Получить список для товаров в корзине."""
        pass

    @abstractmethod
    def create_cart(self, _user: User) -> None:
        """Создать корзину"""
        pass

    @abstractmethod
    def exists(self, _user: User) -> bool:
        """проверяем, что корзина существует и она не пустая"""
        pass
