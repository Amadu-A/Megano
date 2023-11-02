from abc import abstractmethod
from typing import Any

from django.db.models import QuerySet

from catalog_app.models import Product


class IProduct:

    @abstractmethod
    def get_product_top_list(self, const: int) -> QuerySet[Product]:
        """Получить кверисет популярных продуктов"""
        pass

    @abstractmethod
    def get_product_limit_list(self, const: int) -> QuerySet[Product]:
        """Получить кверисет лимитированых продуктов"""
        pass

    @abstractmethod
    def get_sellers_of_product(self, _pk: int) -> list:
        """Получить список продавцов, которые продают данный продукт"""
        pass

    @abstractmethod
    def get_by_id(self, product) -> Product:
        """Получить продукт по id"""
        pass