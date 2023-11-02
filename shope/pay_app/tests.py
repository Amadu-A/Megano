"""Тестирование pay_app"""

import json
from django.test import TestCase
from django.urls import reverse

from auth_app.models import User
from core.enums import OrderStatus

from order_app.utils_test import (
    create_orders_list,
    delete_orders_list,
)
from order_app.models import Order


class PaymentTestCase(TestCase):
    """Тесты оплаты заказа"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(
            username='unittest_user',
            email='usertest@usertest.com',
            password='1q2w3e4r+'
        )

        cls.order = Order.objects.create(
            user=cls.user,
            city='test city',
            address='test address',
            amount=12546,
            payment_id='22d6d597-000f-5000-9000-145f6df21d6f'
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.order.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_new_payment(self):
        """Тест создания оплаты по заказу"""

        response = self.client.get(
            reverse('pay_app:new-pay', kwargs={'pk': self.order.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_success_payment(self):
        """Тест проверки поступления оплаты по заказу"""
        request = {
            "type": "notification",
            "event": "payment.waiting_for_capture",
            "object": {
                "id": "22d6d597-000f-5000-9000-145f6df21d6f",
                "status": "succeeded",
            }
        }
        response = self.client.post(
            reverse('pay_app:success-api'),
            json.dumps(request),
            content_type='application/json')
        order = Order.objects.get(pk=self.order.pk)
        # проверям код 200
        self.assertEqual(response.status_code, 200)
        # проверяем что по заказ поменял статсус на оплачен(оплата прошла)
        self.assertEqual(order.status, OrderStatus.PAID.name)
