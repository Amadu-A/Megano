import random

from beartype import beartype

from django.db.models import QuerySet, Sum, Avg, Min, Max, FloatField, Subquery, OuterRef, F
from django.db.models import Func
from django.db.models.functions import Cast


from catalog_app.models import Product
from core.models import Price
from interface.product_interface import IProduct


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'


class ProductRepository(IProduct):

    def get_product_top_list(self, const: int) -> QuerySet[Product]:
        """Вернуть кверисет популярных продуктов"""
        qs = Product.objects.filter(is_active=True, orderitem__count__gte=1).annotate(
            qty=Sum('orderitem__count'),
            min_price=Round(Cast(Min('price__price'), output_field=FloatField())),
            seller_id=F('price__seller_id')
        ).order_by('-qty')[:const].prefetch_related('discountproduct_set', 'category__discountproduct_set')
        if len(qs) < const:
            min_price_subquery = Price.objects.filter(product=OuterRef('pk')).values('product').annotate(
                min_value=Min('price')
            ).values('min_value')[:1]
            min_price_seller_subquery = Price.objects.filter(
                product=OuterRef('pk'), price=OuterRef('min_price')
            ).values('seller_id')[:1]
            qs = Product.objects.annotate(
                min_price=Subquery(min_price_subquery.values('min_value'), output_field=FloatField()),
                min_price_seller_id=Subquery(min_price_seller_subquery)
            ).filter(min_price__gt=0)[:const].prefetch_related('discountproduct_set', 'category__discountproduct_set')

        return qs

    def get_product_limit_list(self, const: int) -> QuerySet[Product]:
        """Вернуть кверисет лимитированых продуктов"""
        qs = Product.objects.filter(is_active=True, is_limited=True).annotate(
            min_price=Round(Cast(Min('price__price'), output_field=FloatField())),
            max_price=Round(Cast(Max('price__price'), output_field=FloatField())),
            value=Round(Cast(Avg('price__price'), output_field=FloatField()))
        )
        if len(qs) > const:
            const_num_list = random.sample([product.pk for product in qs], const)
            qs = qs.filter(product__id__in=const_num_list)
        return qs.prefetch_related('discountproduct_set', 'category__discountproduct_set')

    @beartype
    def get_sellers_of_product(self, _pk: int) -> list:
        """Получить список продавцов, которые продают данный продукт"""
        distinct = list(Product.objects.filter(pk=_pk).values('price__seller').distinct())
        if distinct[0]['price__seller'] is None:
            return []
        return distinct

    @beartype
    def get_by_id(self, product: str) -> Product:
        """Получить продукт по id"""
        return Product.objects.get(id=product)
