from abc import abstractmethod


from django.db.models import QuerySet

from catalog_app.models import Rewiew
from interface.review_interface import IReview


class ReviewRepository(IReview):

    @abstractmethod
    def get_by_product(self, _pk: int) -> QuerySet[Rewiew]:
        """Получить отзывы по продукту"""
        return Rewiew.objects.filter(product__pk=_pk).select_related('user')
