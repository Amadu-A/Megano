from abc import abstractmethod
from typing import Optional

from beartype.typing import Dict
from django.db.models import QuerySet

from catalog_app.models import DiscountProductGroup


class IDiscountProductGroup:

    @abstractmethod
    def get_list(self) -> QuerySet[DiscountProductGroup]:
        """Получить кверисет скидок на группу продуктов"""
        pass

    @abstractmethod
    def possible_get_discount(self, _cart_item_qs: QuerySet) -> Optional[Dict]:
        """Вернуть возможность применения скидки"""
        pass
