import inject
from django.shortcuts import redirect
from interface.cart_interface import ICart


class CartMixin:
    """Миксин проверки, что корзина пользователя не пустая"""
    _cart = inject.attr(ICart)

    def dispatch(self, request, *args, **kwargs):
        if not self._cart.exists(request.user):
            return redirect('order_app:empty-cart')
        return super().dispatch(request, *args, **kwargs)
