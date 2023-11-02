"""Custom teplates tags"""

from beartype import beartype
from django import template
from core.enums import PayType, DeliveryType, OrderStatus

register = template.Library()


@register.inclusion_tag('includes/order-information.html')
def get_order(order):
    """" Вывод информации по заказу """

    context = {
        'order': order,
        'delivery_type': DeliveryType[order.delivery_type].value,
        'pay_type': PayType[order.pay_type].value,
        'status': OrderStatus[order.status].value
    }
    return context


@register.simple_tag()
def value_delivery_type(name: str) -> str:
    """Получить значение вида доставки по имени"""
    return DeliveryType[name].value


@register.simple_tag()
def value_pay_type(name: str) -> str:
    """Получить значение вида оплаты по имени"""
    return PayType[name].value


@register.simple_tag()
def value_status(name: str) -> str:
    """Получить значение статуса заказа по имени"""
    return OrderStatus[name].value
