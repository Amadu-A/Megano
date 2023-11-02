from abc import abstractmethod
from typing import Optional

from beartype.typing import Dict
from django.db.models import QuerySet

from catalog_app.models import CartSale


class ICartSale:

    @abstractmethod
    def get_list(self) -> QuerySet[CartSale]:
        """Получить кверисет скидок на корзину"""
        pass

    @abstractmethod
    def possible_get_discount(self, _cart_item_qs: QuerySet) -> Optional[CartSale]:
        """Получить кверисет скидок на корзину"""
        pass
