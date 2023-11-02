from abc import abstractmethod

from core.models.base_discount import DiscountBaseModel


class IDiscountBaseModel:

    @abstractmethod
    def save(self, model: DiscountBaseModel) -> None:
        """Сохранить скидку."""
        pass
