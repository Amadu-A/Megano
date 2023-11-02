from django.core.validators import FileExtensionValidator
from django.db import models
from taggit.managers import TaggableManager

from auth_app.models import User
from core.models.base_discount import DiscountBaseModel
from core.models.base_model import BaseModel
from django.utils.translation import gettext_lazy as _


class Category(BaseModel):
    """Модель категории"""
    title = models.CharField(max_length=255, verbose_name=_('title'))
    image = models.FileField(
        null=True,
        blank=True,
        upload_to="images/%Y/%m/%d",
        validators=[FileExtensionValidator(['svg'])],
        verbose_name=_('image'),
        default='/img/icons/allDep.svg'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['id']


class Image(BaseModel):
    """Модель изображения для товара"""
    image = models.ImageField(upload_to="images/%Y/%m/%d", verbose_name=_('image'))

    def __str__(self):
        return f'{self.image}'

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
        ordering = ['id']


class Product(BaseModel):
    """Модель товара"""
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    image = models.ManyToManyField('Image', related_name='image_to_product', verbose_name=_('image'))
    tag = TaggableManager()
    number_of_sales = models.IntegerField(default=0, blank=True, null=False, verbose_name=_('number_of_sales'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('category'))
    is_limited = models.BooleanField(default=True, verbose_name=_('limited'))
    is_delivery = models.BooleanField(default=True, verbose_name=_('delivery'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['id']


class Slider(BaseModel):
    """Модель слайдера. Используется для набора сменяемых баннеров"""
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, verbose_name=_('product')
    )
    description = models.TextField(blank=True, verbose_name=_('description'))
    image = models.ImageField(upload_to="images/%Y/%m/%d", verbose_name=_('image'))

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = _('slider')
        verbose_name_plural = _('sliders')
        ordering = ['id']


class Banner(BaseModel):
    """Модель баннера. Используется для сета баннеров с минимальными ценами в своей категории"""
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('category'))
    image = models.ImageField(upload_to="images/%Y/%m/%d", verbose_name=_('image'))

    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = _('banner')
        verbose_name_plural = _('banners')
        ordering = ['id']


class DiscountProduct(DiscountBaseModel):
    """Модель скидки на товар"""
    image = models.ImageField(upload_to="images/%Y/%m/%d", null=True, verbose_name=_('image'))
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('product'))
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('category'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product discount')
        verbose_name_plural = _('product discounts')
        ordering = ['id']


class DiscountProductGroup(DiscountBaseModel):
    """Модель скидки на группу товаров"""
    image = models.ImageField(upload_to="images/%Y/%m/%d", null=True, verbose_name=_('image'))
    category = models.ManyToManyField('category', verbose_name=_('category as group of products'))
    amount = models.DecimalField(decimal_places=2, max_digits=7, verbose_name=_('fixed amount of discount'))
    fixprice = models.DecimalField(decimal_places=2, max_digits=7, default=1, verbose_name=_('fixed amount of price'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('group of product discount')
        verbose_name_plural = _('group of product discounts')
        ordering = ['id']


class CartSale(DiscountBaseModel):
    """Модель скидки на корзину"""
    image = models.ImageField(upload_to="images/%Y/%m/%d", null=True, verbose_name=_('image'))
    amount = models.DecimalField(
        decimal_places=0, max_digits=7, verbose_name=_('amount of products for a success discount')
    )
    quantity = models.PositiveIntegerField(default=2, verbose_name=_('quantity of products for a success discount'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('cart discount')
        verbose_name_plural = _('cart discounts')
        ordering = ['id']


class Rewiew(BaseModel):
    """Модель отзывов"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'))
    text = models.TextField(verbose_name=_('text'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))

    def __str__(self):
        return f'{self.user} - {self.product}'

    class Meta:
        verbose_name = _('rewiew')
        verbose_name_plural = _('reviews')
        ordering = ['created_at']


###############################################################
# ХАРАКТЕРИСТИКИ ПРОДУКТОВ
###############################################################

class CharacteristicType(BaseModel):
    """Виды характеристик продуктов"""

    name = models.CharField(verbose_name=_('name'),
                            max_length=150
                            )

    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 verbose_name=_('category'),
                                 )

    class Meta:
        """Meta"""
        verbose_name = _('type characteristic of product')
        verbose_name_plural = _('types characteristic of product')

    def __str__(self):
        """Строковое представление"""
        return f'{self.name}'


class CharacteristicValue(BaseModel):
    """Значение характеристики продукта"""
    characteristic_type = models.ForeignKey(CharacteristicType,
                                            on_delete=models.CASCADE,
                                            verbose_name=_('type of characteristic'),
                                            related_name='characteristic_value'
                                            )
    value = models.CharField(verbose_name=_('value'),
                             max_length=100
                             )

    class Meta:
        """Meta"""
        verbose_name = _('characteristic value')
        verbose_name_plural = _('characteristic values')

    def __str__(self):
        """Строковое представление"""
        return f'{self.characteristic_type}-{self.value}'


class CharacteristicProduct(BaseModel):
    """Значение характеристики в продукте"""
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name=_('product'),
                                related_name='characteristics'
                                )

    characteristic_value = models.ForeignKey(CharacteristicValue,
                                             on_delete=models.CASCADE,
                                             verbose_name=_('value of characteristic'),
                                             related_name='characteristics'
                                             )

    class Meta:
        """Meta"""
        verbose_name = _('characteristic of product')
        verbose_name_plural = _('characteristics of product')

    def __str__(self):
        """Строковое представление"""
        return f'{self.product} - {self.characteristic_value}'


class ProductViewed(BaseModel):
    """Модель просмотренных товаров"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))

    def __str__(self):
        return f'Товар {self.product} просмотрен {self.user}'

    class Meta:
        verbose_name = _('viewed product')
        verbose_name_plural = _('viewed products')
        ordering = ['id']


class CompareProduct(BaseModel):
    """Модель товаров для сравнения"""
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name=_('session key'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))

    def __str__(self):
        return f'Товар {self.product}'

    class Meta:
        verbose_name = _('product for comparison')
        verbose_name_plural = _('products for comparison')
        ordering = ['id']
