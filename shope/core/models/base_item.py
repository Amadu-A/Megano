from django.db import models
from django.utils.translation import gettext_lazy as _
from catalog_app.models import Product
from .base_model import BaseModel
from .seller import Seller


class BaseModelItem(BaseModel):

    """
    Базовая модель для корзины и заказов.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name=_('seller'))
    count = models.IntegerField(verbose_name=_('count product'))
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_('amount'))

    class Meta:
        abstract = True
