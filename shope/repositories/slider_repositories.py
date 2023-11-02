from django.db.models import QuerySet
import random

from catalog_app.models import Slider
from interface.slider_interface import ISlider


class SliderRepository(ISlider):

    def get_slider_list(self, const: int) -> QuerySet[Slider]:
        """Вернуть кверисет слайдеров"""
        qs = Slider.objects.filter(is_active=True).select_related('product')
        if len(qs) > const:
            const_num_list = random.sample([slider.product.pk for slider in qs], const)
            qs = qs.filter(product__id__in=const_num_list)
        return qs
