from django.db import models

from core.models import BaseModelItem
from core.models.base_model import BaseModel
from auth_app.models import User
from django.utils.translation import gettext_lazy as _


class Cart(BaseModel):
    """
    Модель корзины пользователя.
    """

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name=_('user'),
                             related_name='carts')

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f'{self.pk}-{self.user} - active({self.is_active})'


class CartItem(BaseModelItem):
    """
    Модель для хранения товаров в корзине.
    """
    discount = models.DecimalField(decimal_places=2, max_digits=7, default=0,
                                   blank=True, null=True, verbose_name=_('discount'))
    total_amount = models.DecimalField(decimal_places=2, max_digits=7, default=0,
                                       blank=True, null=True, verbose_name=_('amount with discount'))
    cart_id = models.ForeignKey(Cart,
                                on_delete=models.CASCADE,
                                verbose_name=_('cart'),
                                related_name='cartitems')

    class Meta:
        verbose_name = _('CartItem')
        verbose_name_plural = _('CartItems')

    def __str__(self):
        return f'{self.cart_id} - {self.product}'
