from django.test import TestCase
from django.urls import reverse

from auth_app.models import User

from random import choice

from cart_app.models import CartItem
from core.models import Price
from order_app.utils_test import (
    create_categories_list,
    delete_categories_list,
    create_products_list,
    delete_products_list,
    create_seller,
    delete_seller,
    create_cart,
    delete_cart,
    create_cart_items,
    delete_cart_items


)


class AddProductToCartTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(
            username='unittest_user',
            email='usertest@usertest.com',
            password='1q2w3e4r+'
        )
        cls.category = create_categories_list()
        cls.products = create_products_list(categoies=cls.category)
        cls.seller = create_seller(cls.user)
        cls.cart = create_cart(cls.user)

        cls.product = choice(cls.products)
        cls.cart_data = {

            'product': cls.product.id,
            'product_name': cls.product.name,
            'image': 'hello_wold',
            'count': '1',
            'amount': '1250.00',
            'seller': cls.seller.pk,

        }
    @classmethod
    def tearDownClass(cls):
        delete_seller(cls.seller)
        delete_products_list(cls.products)
        delete_categories_list(cls.category)
        delete_cart(cls.cart)
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_add_product_to_cart(self):
        response = self.client.post(
            headers={'X-Requested-With': 'XMLHttpRequest'},
            path=reverse('cart_app:catalog_add'),
            data=self.cart_data),

        self.assertTrue(CartItem.objects.filter(cart_id=self.cart, product=self.product).exists())
        self.assertTrue(CartItem.objects.filter(cart_id=self.cart, product=self.product).first().amount, 1250.00)

    def test_add_product_to_cart_for_anonymous(self):
        self.client.logout()
        response = self.client.post(
            headers={'X-Requested-With': 'XMLHttpRequest'},
            path=reverse('cart_app:catalog_add'),
            data=self.cart_data)
        self.assertTrue(self.client.session, 'cart')
        self.assertTrue(self.client.session['cart'], self.cart_data)

class ChangeCountProductTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(
            username='unittest_user',
            email='usertest@usertest.com',
            password='1q2w3e4r+'
        )
        cls.category = create_categories_list()
        cls.products = create_products_list(categoies=cls.category)
        cls.seller = create_seller(cls.user)
        cls.cart = create_cart(cls.user)
        cls.product = choice(cls.products)
        cls.price = Price.objects.create(price=1250.00, product=cls.product, seller=cls.seller)
        cls.cartitem = CartItem.objects.create(
            cart_id=cls.cart,
            product=cls.product,
            seller=cls.seller,
            count=1,
            amount=1250.00)

        cls.cart_data = {
            'product': cls.product.id,
            'count': '1',
            'seller': cls.seller.pk,

        }

    @classmethod
    def tearDownClass(cls):
        delete_seller(cls.seller)
        delete_products_list(cls.products)
        delete_categories_list(cls.category)
        delete_cart(cls.cart)
        cls.cartitem.delete()
        cls.price.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_change_count_product(self):
        response = self.client.post(
            headers={'X-Requested-With': 'XMLHttpRequest'},
            path=reverse('cart_app:change_count'),
            data=self.cart_data)

        self.assertTrue(CartItem.objects.filter(cart_id=self.cart, product=self.product).first().count, 2)

class DeleteCartItemTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(
            username='unittest_user',
            email='usertest@usertest.com',
            password='1q2w3e4r+'
        )
        cls.category = create_categories_list()
        cls.products = create_products_list(categoies=cls.category)
        cls.seller = create_seller(cls.user)
        cls.cart = create_cart(cls.user)
        cls.product = choice(cls.products)
        cls.cartitem = CartItem.objects.create(
            cart_id=cls.cart,
            product=cls.product,
            seller=cls.seller,
            count=1,
            amount=1250.00)

        cls.cart_data = {
            'product': cls.product.id
        }

    @classmethod
    def tearDownClass(cls):
        delete_seller(cls.seller)
        delete_products_list(cls.products)
        delete_categories_list(cls.category)
        delete_cart(cls.cart)
        cls.cartitem.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_delete_cartitem(self):
        response = self.client.post(
            headers={'X-Requested-With': 'XMLHttpRequest'},
            path=reverse('cart_app:item_delete'),
            data=self.cart_data)

        self.assertFalse(CartItem.objects.filter(cart_id=self.cart, product=self.product).exists())