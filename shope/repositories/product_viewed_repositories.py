from typing import Optional

from beartype import beartype
from django.db.models import QuerySet

from catalog_app.models import ProductViewed
from interface.product_viewed_interface import IProductViewed


class ProductViewedRepository(IProductViewed):

    @beartype
    def get_product_viewed_list(self, _user_id: int) -> QuerySet[ProductViewed]:
        """Вернуть кверисет просмотренных продуктов"""
        return ProductViewed.objects.filter(user_id=_user_id)

    @beartype
    def create_product_viewed(self, _user_id: int, _product_id: int) -> None:
        """Создать объект просмотренного продукта"""
        ProductViewed.objects.create(user_id=_user_id, product_id=_product_id)

    @beartype
    def get_product_viewed_by_id(self, _user_id: int, _product_id: int) -> Optional[ProductViewed]:
        """Получить объект просмотренного продукта"""
        try:
            product = ProductViewed.objects.get(user_id=_user_id, product_id=_product_id)
        except ProductViewed.DoesNotExist:
            product = None
        return product

    @beartype
    def delete_product_viewed_by_id(self, _user_id: int, _product_id: int) -> None:
        """Удалить объект просмотренного продукта"""
        ProductViewed.objects.get(user_id=_user_id, product_id=_product_id).delete()
