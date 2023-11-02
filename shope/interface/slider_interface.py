from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import Slider


class ISlider:

    @abstractmethod
    def get_slider_list(self, const: int) -> QuerySet[Slider]:
        """Получить кверисет слайдеров"""
        pass
