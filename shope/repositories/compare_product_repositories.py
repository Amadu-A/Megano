from beartype import beartype
from django.utils import timezone
from django.db.models import QuerySet

from catalog_app.models import CompareProduct, CharacteristicType
from interface.compare_product_interface import ICompareProduct


today = timezone.now().date()


class CompareProductRepository(ICompareProduct):

    @beartype
    def get_compare_product_list(self, _session_key: str) -> QuerySet[CompareProduct]:
        """Вернуть кверисет продуктов для сравнения"""
        qs = CompareProduct.objects.filter(session_key=_session_key).prefetch_related(
            'product__category__characteristictype_set',
            'product__characteristics'
        )
        return qs

    @beartype
    def create_compare_product(self, _product_id: int, _session_key: str) -> None:
        """Создать продукт для сравнения"""
        CompareProduct.objects.create(product_id=_product_id, session_key=_session_key)

    @beartype
    def possible_compare_product(self, _product_id: int, _session_key: str) -> bool:
        """Проверить возможность сравнения"""
        char_qs = CharacteristicType.objects.filter(category__product__id=_product_id)
        qs = CompareProduct.objects.filter(session_key=_session_key, product__category__characteristictype__in=char_qs)
        if qs:
            return True
        return False

    @beartype
    def delete_compare_product_by_id(self, _compare_product_id: int, _session_key: str) -> None:
        """Удалить продукт из списка сравнения"""
        CompareProduct.objects.get(id=_compare_product_id, session_key=_session_key).delete()
