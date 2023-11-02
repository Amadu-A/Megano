"""Order app"""
from django.apps import AppConfig


class OrderAppConfig(AppConfig):
    """ Order app config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_app'
