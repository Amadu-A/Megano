from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import Rewiew


class IReview:

    @abstractmethod
    def get_by_product(self, _pk: int) -> QuerySet[Rewiew]:
        """Получить отзывы по продукту"""
        pass
