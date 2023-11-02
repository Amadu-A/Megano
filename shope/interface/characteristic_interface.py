""" Интерфейс характеристик продуктов"""
from abc import abstractmethod

from django.db.models import QuerySet
from catalog_app.models import CharacteristicProduct, Product


class ICharacteristicProduct:
    """Класс-интерфейс характеристик продукта"""

    @abstractmethod
    def get_by_product(self, _product: Product) -> QuerySet[CharacteristicProduct]:
        """Получить характеристики по продукту."""
        pass
