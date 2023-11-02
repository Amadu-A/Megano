""" Интерфейс фильтрации каталога"""
from abc import abstractmethod
from typing import Any, Optional
from django.db.models import QuerySet

from catalog_app.models import Product


class ICatalogFilter:
    """Класс-репозиторий фильтрации товаров"""

    @abstractmethod
    def get_filtered_products(self, product_name: Optional[str or None],
                              free_delivery: Optional[bool or None],
                              is_limited: Optional[bool or None],
                              product_min_price: Optional[str or None],
                              product_max_price: Optional[str or None]) -> QuerySet[Product]:
        """Получить отфильтрованные продукты"""
        pass

    @abstractmethod
    def filter_by_tag(self, tag: str) -> QuerySet[Product]:
        """Получить отфильтрованные продукты по тегам"""
        pass

    @abstractmethod
    def filter_by_sort(self, sort: str, query: QuerySet[Product]) -> QuerySet[Product]:
        """Получить отфильтрованные продукты по критериям сортировки"""
        pass

    @abstractmethod
    def get_filtered_products_by_category(self, _category_id: str) -> QuerySet[Product]:
        """Получить отфильтрованные по категории продукты"""
        pass

    @abstractmethod
    def get_filtered_products_by_char(self, _char_id: str) -> QuerySet[Product]:
        """Получить отфильтрованные по Характеристике продукты"""
        pass
