"""Статус заказа enum."""

from django.utils.translation import gettext_lazy as _

from .base_enum import Choices


class OrderStatus(Choices):
    """Перечисления (статус оплаты)"""
    NOT_PAID = _('is not paid')
    PAID = _('is paid')
    DELIVERY = _('is delivered')
    CLOSE = _('is closed')
