import random

from django.db.models import QuerySet, Min, Func, FloatField
from django.db.models.functions import Cast

from catalog_app.models import Banner
from interface.banner_interface import IBanner


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'


class BannerRepository(IBanner):

    def get_banner_list(self, const: int) -> QuerySet[Banner]:
        """Вернуть кверисет баннеров"""
        qs = Banner.objects.filter(is_active=True).select_related('category')
        if len(qs) > const:
            const_num_list = random.sample([banner.category.pk for banner in qs], const)
            qs = qs.filter(category__id__in=const_num_list)
        return qs.annotate(min_price=Round(Cast(Min('category__product__price__price'), output_field=FloatField())))
