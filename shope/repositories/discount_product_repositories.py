from django.db.models import QuerySet, Q, DateTimeField
from django.db.models.functions import Cast
from django.utils import timezone

from catalog_app.models import DiscountProduct
from interface.discount_product_interface import IDiscountProduct


today = Cast(timezone.now().date(), output_field=DateTimeField())


class DiscountProductRepository(IDiscountProduct):

    def get_list(self) -> QuerySet[DiscountProduct]:
        """Вернуть кверисет скидок на продукт"""
        return DiscountProduct.objects.filter(
            is_active=True,
            data_end__gte=today,
            data_start__lte=today
        )

    def get_list_by_id(self, _id: int) -> QuerySet[DiscountProduct]:
        """Вернуть кверисет скидок на продукт по id"""
        return DiscountProduct.objects.filter(is_active=True, data_end__gte=today, data_start__lte=today).filter(
            Q(product__id=_id) | Q(category__product__id=_id)
        )
