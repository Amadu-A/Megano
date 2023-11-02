from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from core.utils.exception import MaxDiscountErrorException, MinDiscountErrorException
from .base_model import BaseModel


class DiscountBaseModel(BaseModel):
    """Базовая модель для скидок"""
    name = models.CharField(max_length=255, verbose_name=_('discount name'))
    priority = models.PositiveIntegerField(default=1, verbose_name=_('priority'))
    value = models.IntegerField(default=0, verbose_name=_('sale value'))
    data_start = models.DateField(default=timezone.now, verbose_name=_('date of discount start'))
    data_end = models.DateField(default=timezone.now, verbose_name=_('date of discount end'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.value >= 99:
            raise MaxDiscountErrorException
        if self.value < 0:
            raise MinDiscountErrorException
        super().save(*args, **kwargs)
