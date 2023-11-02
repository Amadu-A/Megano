"""Signals for profile"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """create Profile after User created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    """Upadate Profile after User updated"""
    Profile.objects.update_or_create(user=instance)
