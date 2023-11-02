from abc import abstractmethod
from beartype.typing import List, Dict

from core.models import Price


class IPrice:

    @abstractmethod
    def get_last_minprice_dct(self, _product_id_lst: List) -> List[Dict] | None:
        """Получить последнюю цену  продукта"""
        pass

    def save(self, model: Price) -> None:
        """Сохранить цену."""
        pass

    @abstractmethod
    def get_by_product_and_seller(self, product_id: str, seller_id) -> Price:
        """Получить цену по продукту и продавцу"""
        pass