from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """User model"""

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    username = models.CharField(unique=True, default="", max_length=48, null=False, blank=False)
    email = models.EmailField(unique=True, default="", null=False, blank=False)
    middle_name = models.CharField(verbose_name=_('Full name'), default="", null=False, blank=False, max_length=48)
    activation_key = models.CharField(default="", null=False, blank=False, max_length=48)
    activation_key_set = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_activation_key_expired = models.BooleanField(default=False, blank=True, null=True)

    @staticmethod
    def activation_key_expired(self):
        if now() <= self.activation_key_set + timedelta(hours=48):
            return False
        return True
