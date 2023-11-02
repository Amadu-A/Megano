"""Репозитарий Cart"""
from typing import Optional
from decimal import Decimal
from beartype import beartype
from django.db.models import Sum
from interface.cart_interface import ICart
from auth_app.models import User
from cart_app.models import Cart


class CartRepository(ICart):
    """CartItemRepository"""

    @beartype
    def get_active_by_user(self, _user: User) -> Optional[Cart]:
        """Получить активную корзину пользоветеля."""
        try:
            return Cart.objects.get(user=_user, is_active=True)
        except Cart.DoesNotExist:
            return None

    @beartype
    def save(self, model: Cart) -> None:
        """ Сохранить корзину."""
        model.save()

    @beartype
    def total_amount(self, model: Cart) -> Optional[Decimal]:
        """ Получить сумму товаров в корзине."""
        cart = Cart.objects.annotate(
            total_amount=Sum('cartitems__amount', default=0)
        ).get(pk=model.pk)
        return Decimal(round(cart.total_amount, 2))

    @beartype
    def model_to_list(self, model: Cart) -> Optional[list]:
        """ Получить список для товаров в корзине."""
        res = []
        for i_product in model.cartitems.all():
            res.append({'product': i_product.product,
                        'seller': i_product.seller,
                        'count': i_product.count,
                        'amount': i_product.amount
                        }
                       )

        return res

    @beartype
    def create_cart(self, _user: User):
        """Создать корзину"""
        return Cart.objects.create(user=_user)

    @beartype
    def exists(self, _user: User) -> bool:
        """проверяем, что корзина существует и она не пустая"""
        return Cart.objects.filter(user=_user, is_active=True).exists()
