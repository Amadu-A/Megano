"""Служебные функции для тестирования order_app"""

from string import ascii_letters
from random import choices, randint, choice

from auth_app.models import User
from order_app.models import Order
from catalog_app.models import Category, Product
from core.models import Seller
from cart_app.models import Cart, CartItem


def create_orders_list(user) -> list[Order]:
    """Создание списка новых заказов"""

    return [Order.objects.create(
            user=user,
            city=''.join(choices(ascii_letters, k=10)),
            address=''.join(choices(ascii_letters, k=10)),
            amount=randint(500, 9000)
            )
            for _ in range(10)]


def delete_orders_list(orders_list: list[Order]) -> None:
    """Удаление заказов из списка"""

    for i_order in orders_list:
        i_order.delete()


def create_categories_list() -> list[Category]:
    """Создание категорий"""

    categories = (Category(title=''.join(choices(ascii_letters, k=10)))
                  for _ in range(5)
                  )
    return Category.objects.bulk_create(categories)


def delete_categories_list(categories_list: list[Category]) -> None:
    """удаление категорий"""

    for i_category in categories_list:
        i_category.delete()


def create_products_list(categoies: list[Category]) -> list[Product]:
    """Создание продуктов"""
    products = (Product(
        title=''.join(choices(ascii_letters, k=10)),
        name=''.join(choices(ascii_letters, k=10)),
        category=choice(categoies))
        for _ in range(10)
    )
    return Product.objects.bulk_create(products)


def delete_products_list(products_list: list[Product]) -> None:
    """удаление списка продуктов"""

    for i_product in products_list:
        i_product.delete()


def create_cart(user: User) -> Cart:
    """Создание корзины"""
    return Cart.objects.create(user=user)


def delete_cart(cart: Cart) -> None:
    """Удаление корзины"""
    cart.delete()


def create_seller(user: User) -> Seller:
    """Создание продавца"""
    return Seller.objects.create(
        name=''.join(choices(ascii_letters, k=10)),
        user=user
    )


def delete_seller(seller: Seller) -> None:
    """Удаление продавца"""
    seller.delete()


def create_cart_items(products: list[Product], cart: Cart, seller: Seller) -> list[CartItem]:
    """Заполнение корзины продуктами"""
    cart_items = (CartItem(
        cart_id=cart,
        product=i_product,
        seller=seller,
        count=randint(1, 10),
        amount=randint(500, 10000))
        for i_product in products
    )
    return CartItem.objects.bulk_create(cart_items)


def delete_cart_items(carts_list: list[CartItem]) -> None:
    """удаление продуктов из корзины"""

    for i_cart_item in carts_list:
        i_cart_item.delete()
