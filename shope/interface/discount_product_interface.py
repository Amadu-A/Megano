from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import DiscountProduct


class IDiscountProduct:

    @abstractmethod
    def get_list(self) -> QuerySet[DiscountProduct]:
        """Получить кверисет скидок"""
        pass

    @abstractmethod
    def get_list_by_id(self, _id: int) -> QuerySet[DiscountProduct]:
        """Получить кверисет скидок на продукт по id"""
        pass
