"""Виды оплтаты enum."""

from django.utils.translation import gettext_lazy as _

from .base_enum import Choices


class PayType(Choices):
    """Перечисления (виды оплаты)"""
    bank_card = _('bank card')
    spb = _('spb')
