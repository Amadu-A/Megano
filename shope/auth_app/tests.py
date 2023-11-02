from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User


class RegisterTestCase(TestCase):

    @classmethod
    def setUp(cls):
        cls.user = {
            'first_name': 'Alexandr',
            'last_name': 'Calinin',
            'username': 'Alexandr1',
            'email': 'kalininsasa38@gmail.com',
            'password1': 'Alex23456',
            'password2': 'Alex23456',
        }

    def test_registration(self):
        response1 = self.client.post(path=reverse('auth_app:register'), data=self.user)
        self.assertEqual(response1.status_code, 302)
        self.assertTrue(User.objects.filter(email=self.user.get('email')).exists())

        response2 = self.client.get(reverse('auth_app:confirm-email'))
        self.assertEqual(response2.status_code, 200)

        response3 = self.client.get(reverse_lazy('home'))
        self.assertEqual(response3.status_code, 200)


class LoginTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='Ales',
            email='afaf@gmail.com',
            password='Alex6514537',
        )

    def tearDown(self):
        self.user.delete()

    def test_login(self):
        response1 = self.client.get(reverse('auth_app:login'))
        self.assertEqual(response1.status_code, 200)
        self.assertTrue(User.objects.filter(email=self.user.email).exists())
        self.client.force_login(self.user)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        response2 = self.client.post(reverse_lazy('auth_app:login'))
        self.assertEqual(response2.status_code, 302)


class LogoutTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(
            username='Ales',
            email='afaf@gmail.com',
            password='Alex6514537',
        )

    def setUp(self):
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_logout(self):
        self.assertTrue(User.objects.filter(email=self.user.email).exists())
        response = self.client.post(reverse('auth_app:logout'))
        self.assertEqual(response.status_code, 302)


class SetNewPasswordTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(
            username='Ales',
            email='afaf@gmail.com',
            password='Alex6514537',
        )
        cls.user.is_activation_key_expired = False
        cls.user.is_active = True

    def setUp(self):
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_set_new_password(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self.user)
        response1 = self.client.post(reverse('auth_app:restore_password',
                                             kwargs={'uidb64': uidb64, 'token': token}))
        self.assertIn(uidb64, response1.url)
        self.assertEqual(response1.status_code, 302)
