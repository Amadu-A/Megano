from django.db.models import QuerySet

from catalog_app.models import Category
from interface.category_interface import ICategory


class CategoryRepository(ICategory):

    def get_category_list(self) -> QuerySet[Category]:
        """Вернуть кверисет категорий"""
        return Category.objects.all().prefetch_related('characteristictype_set')
