"""Тестирование profile_app"""

from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache

from auth_app.models import User


class ProfileTestCase(TestCase):
    """Тесты оплаты заказа"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(
            username='unittest_user',
            email='usertest@usertest.com',
            password='1q2w3e4r+'
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cache.clear()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_detail_profile_view(self):
        """Тест получение страницы профайла"""

        response = self.client.get(
            reverse('profile')
        )
        context_data = response.context_data
        # проверяем, что нужная страница отркрылась
        self.assertEqual(response.status_code, 200)
        # проверяем, что профайл имено заданного пользователя
        self.assertEqual(context_data['profile'], self.user.profile)
