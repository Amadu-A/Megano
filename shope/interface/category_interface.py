from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import Category


class ICategory:

    @abstractmethod
    def get_category_list(self) -> QuerySet[Category]:
        """Получить кверисет категорий"""
        pass
