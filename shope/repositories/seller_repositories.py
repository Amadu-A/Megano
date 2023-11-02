""" Репозиторий продавцы"""
from typing import Any
from beartype import beartype

from core.models.seller import Seller
from interface.seller_interface import ISeller


class SellerRepository(ISeller):

    @beartype
    def get_by_id(self, id: str) -> Seller:
        """Получить Селлера по id"""
        return Seller.objects.get(id=id)

    @beartype
    def get_last_price_of_product(self, _pk: int, _product_pk: int) -> dict[str, Any] | None:
        """Получить последнюю цену  продукта"""
        res = Seller.objects.filter(pk=_pk, product_seller__product=_product_pk).values(
            'pk', 'name', 'product_seller__price').order_by(
                'product_seller__date').last()
        return res
