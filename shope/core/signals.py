"""Signals for cache"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from core.utils.cache import delete_cache_setup

from core.models.cache_setup import CacheSetup
from catalog_app.models import Rewiew, Product, Category, Banner
from order_app.models import OrderItem
from .utils.cache_key import (
    DETAIL_PRODUCT_KEY,
    CATEGORY_LIST_KEY,
    BANNER_LIST_KEY,
    TOP_PRODUCT_LIST_KEY,
    PRODUCTS_KEY,
    CATALOG_CATEGORY
)


@receiver(post_save, sender=CacheSetup)
def cache_setup_change(sender, instance, **kwargs):
    """Изменение настроек кеша.
    Удаляем кеш настроек"""

    delete_cache_setup()


@receiver(post_save, sender=Rewiew)
def review_change(sender, instance, **kwargs):
    """ Создание отзыва.
    Удаляем кеш детальной страницы продукта на странице которого создан отзыв"""
    # invalidate_cache('product', instance.product_id)
    key = DETAIL_PRODUCT_KEY + str(instance.product_id)
    if cache.get(key):
        cache.delete(key)

    key = make_template_fragment_key('detail_product', (instance.product_id,))
    if key:
        cache.delete(key)


@receiver(post_save, sender=Product)
def product_change(sender, instance, **kwargs):
    """Изменение продукта.
    Удаляем кеш продукта"""

    key = DETAIL_PRODUCT_KEY + str(instance.pk)
    if cache.get(key):
        cache.delete(key)

    if cache.get(PRODUCTS_KEY):
        cache.delete(PRODUCTS_KEY)

    key = CATALOG_CATEGORY + str(instance.category.pk)
    if cache.get(key):
        cache.delete(key)

    if cache.get(CATALOG_CATEGORY):
        cache.delete(CATALOG_CATEGORY)

    key = make_template_fragment_key('detail_product', (instance.pk,))
    if key:
        cache.delete(key)


@receiver(post_save, sender=Category)
def category_change(sender, instance, **kwargs):
    """Изменение категории.
    Удаляем кеш категории из контекст-процессора"""

    if cache.get(CATEGORY_LIST_KEY):
        cache.delete(CATEGORY_LIST_KEY)


@receiver(post_save, sender=Banner)
def banner_change(sender, instance, **kwargs):
    """Изменение  банера.
    Удаляем кеш банера"""

    if cache.get(BANNER_LIST_KEY):
        cache.delete(BANNER_LIST_KEY)


@receiver(post_save, sender=OrderItem)
@receiver(post_save, sender=Product)
def top_product_change(sender, instance, **kwargs):
    """Отслеживаем изменениен продукта и изменение заказа.
    Удаляем кеш топ-товаров"""

    if cache.get(TOP_PRODUCT_LIST_KEY):
        cache.delete(TOP_PRODUCT_LIST_KEY)
