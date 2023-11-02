"""Order_app models"""
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, BaseModelItem
from core.enums import PayType, DeliveryType, OrderStatus


class Order(BaseModel):
    """Модель заказа"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name=_('user'),
                             related_name='order',
                             )

    city = models.CharField(verbose_name=_('city'),
                            max_length=30)

    address = models.CharField(verbose_name=_('address'),
                               max_length=200)

    pay_type = models.CharField(verbose_name=_('payment type'),
                                choices=PayType.choices,
                                max_length=10,
                                default=PayType.bank_card.name
                                )

    delivery_type = models.CharField(verbose_name=_('delivery type'),
                                     choices=DeliveryType.choices,
                                     max_length=10,
                                     default=DeliveryType.REGULAR.name
                                     )

    status = models.CharField(verbose_name=_('status'),
                              choices=OrderStatus.choices,
                              max_length=10,
                              default=OrderStatus.NOT_PAID.name
                              )

    amount = models.DecimalField(verbose_name=_('order amount'),
                                 default=Decimal('0.0'),
                                 decimal_places=2,
                                 max_digits=15)

    payment_id = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        """Meta class"""
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self) -> str:
        """Строкое представление."""
        return '{order} № {order_number} {date}: {order_date}'.format(
            order=_('order'),
            order_number=(self.pk),
            date=_('from'),
            order_date=self.created_at.strftime('%d.%m.%y')
        )


class OrderItem(BaseModelItem):
    """Модель товаров в заказе"""

    order = models.ForeignKey(Order,
                              verbose_name=_('order'),
                              on_delete=models.CASCADE,
                              related_name='order_item')

    class Meta:
        verbose_name = _('OrderItem')

    def __str__(self):
        return f'{self.order} - {self.product}'
