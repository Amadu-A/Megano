"""Виды доставки enum."""

from django.utils.translation import gettext_lazy as _

from .base_enum import Choices


class DeliveryType(Choices):
    """Перечисления (виды доставки)"""
    EXPRESS = _('express delivery')
    REGULAR = _('regular delivery')
