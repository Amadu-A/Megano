from typing import Optional

from beartype import beartype
from django.db.models import QuerySet, Sum, DateTimeField
from django.db.models.functions import Cast
from django.utils import timezone

from catalog_app.models import CartSale
from interface.cart_sale_interface import ICartSale


today = Cast(timezone.now().date(), output_field=DateTimeField())


class CartSaleRepository(ICartSale):

    @beartype
    def get_list(self) -> QuerySet[CartSale]:
        """Вернуть кверисет скидок на продукт"""
        return CartSale.objects.filter(
            is_active=True,
            data_end__gte=today,
            data_start__lte=today
        )

    @beartype
    def possible_get_discount(self, _cart_item_qs: QuerySet) -> Optional[CartSale]:
        """Вернуть возможность применения скидки"""
        qs = _cart_item_qs.values('product__id', 'count', 'amount')
        total_amount = sum([dct['amount'] for dct in qs])
        total_count = _cart_item_qs.aggregate(num=Sum('count'))
        total_count = total_count['num']
        if not total_count:
            total_count = 0
        sale_qs = self.get_list().filter(quantity__lte=total_count, amount__lte=total_amount).order_by('-value').first()
        if not sale_qs:
            return None
        return sale_qs
