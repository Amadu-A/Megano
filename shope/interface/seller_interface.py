""" Интерфейс продавцы"""
from abc import abstractmethod
from typing import Any

from core.models.seller import Seller


class ISeller:

    @abstractmethod
    def get_by_id(self, id: str) -> Seller:
        """Получить продавца по id"""
        pass


    @abstractmethod
    def get_last_price_of_product(self, _pk: int, _product_pk: int) -> dict[str, Any]:
        """Получить последнюю цену  продукта"""
        pass
