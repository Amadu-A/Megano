from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import ProductViewed


class IProductViewed:

    @abstractmethod
    def get_product_viewed_list(self, _user_id: int) -> QuerySet[ProductViewed]:
        """Получить кверисет просмотренных продуктов"""
        pass

    @abstractmethod
    def create_product_viewed(self, _user_id: int, _product_id: int) -> None:
        """Создать объект просмотренного продукта"""
        pass

    @abstractmethod
    def get_product_viewed_by_id(self, _user_id: int, _product_id: int) -> ProductViewed:
        """Получить объект просмотренного продукта"""
        pass

    @abstractmethod
    def delete_product_viewed_by_id(self, _user_id: int, _product_id: int) -> None:
        """Удалить объект просмотренного продукта"""
        pass
