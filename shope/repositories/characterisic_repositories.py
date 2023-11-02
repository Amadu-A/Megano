"""Репозиторий харакеристик продуктов"""
from beartype import beartype
from django.db.models import QuerySet

from interface.characteristic_interface import ICharacteristicProduct
from catalog_app.models import CharacteristicProduct, Product


class CharacteristicRepository(ICharacteristicProduct):
    """Класс репозиторий характристик"""

    @beartype
    def get_by_product(self, _product: Product) -> QuerySet[CharacteristicProduct]:
        """Получить характеристики по продукту."""

        return CharacteristicProduct.objects.filter(product=_product).select_related('characteristic_value')
