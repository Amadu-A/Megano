from django.db import models
from django.conf import settings
from .base_model import BaseModel
from django.utils.translation import gettext_lazy as _


class Seller(BaseModel):
    """Модель продавцов товаров"""
    name = models.CharField(verbose_name=_('name'),
                            max_length=120)

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name=_('user'),
                                related_name='seller',
                                )

    class Meta:
        """Meta class"""
        verbose_name = _('seller')
        verbose_name_plural = _('sellers')

    def __str__(self) -> str:
        """Строкое представление."""
        return self.name