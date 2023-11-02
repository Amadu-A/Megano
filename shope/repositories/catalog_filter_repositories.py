""" Репозиторий фильтрации каталога"""
from typing import Any, Optional

from beartype import beartype
from django.db.models import QuerySet, OuterRef, Min, Subquery, Count, FloatField
from taggit.models import Tag

from catalog_app.models import Product
from core.models.price import Price


class CatalogFilterRepository:
    """Класс-интерфейс фильтрации товаров"""
    min_price_subquery = Price.objects.filter(product=OuterRef('pk')).values('product').annotate(
        min_value=Min('price')
    ).values('min_value')[:1]
    min_price_seller_subquery = Price.objects.filter(
        product=OuterRef('pk'), price=OuterRef('min_price')
    ).values('seller_id')[:1]
    queryset = Product.objects.annotate(
        min_price=Subquery(min_price_subquery.values('min_value'), output_field=FloatField()),
        min_price_seller_id=Subquery(min_price_seller_subquery)
    ).filter(min_price__gt=0).prefetch_related('discountproduct_set', 'category__discountproduct_set')

    @beartype
    def get_filtered_products(self, product_name: Optional[str or None],
                              free_delivery: Optional[bool or None],
                              is_limited: Optional[bool or None],
                              product_min_price: Optional[str or None],
                              product_max_price: Optional[str or None]) -> QuerySet[Product]:
        """Получить отфильтрованные продукты"""

        if product_name is not None:
            if free_delivery and is_limited:
                return self.queryset.filter(title__icontains=product_name.title(), is_delivery=free_delivery,
                                            is_active=is_limited,
                                            min_price__range=(product_min_price, product_max_price))

            elif free_delivery:
                return self.queryset.filter(title__icontains=product_name.title(), is_delivery=free_delivery,
                                            min_price__range=(product_min_price, product_max_price))

            elif is_limited:
                return self.queryset.filter(title__icontains=product_name.title(), is_active=is_limited,
                                            min_price__range=(product_min_price, product_max_price))

            elif product_name and product_min_price or product_max_price:
                return self.queryset.filter(title__icontains=product_name.title(),
                                            min_price__range=(product_min_price, product_max_price))

            else:
                return self.queryset.filter(title__icontains=product_name.title())
        else:
            if free_delivery and is_limited:
                return self.queryset.filter(is_delivery=free_delivery, is_active=is_limited,
                                            min_price__range=(product_min_price, product_max_price))

            elif free_delivery:
                return self.queryset.filter(is_delivery=free_delivery,
                                            min_price__range=(product_min_price, product_max_price))

            elif is_limited:
                return self.queryset.filter(is_active=is_limited,
                                            min_price__range=(product_min_price, product_max_price))
            else:
                if not isinstance(product_min_price, str):
                    return self.queryset
                else:
                    return self.queryset.filter(min_price__range=(product_min_price, product_max_price))

    @beartype
    def filter_by_tag(self, tag_name: str) -> QuerySet[Product]:
        tags = Tag.objects.filter(slug=tag_name).values_list('name', flat=True)
        return self.queryset.filter(tag__name__in=tags)

    @beartype
    def filter_by_sort(self, sort: str, query: QuerySet[Product]) -> QuerySet[Product]:
        if sort == "min_price":
            return query.order_by(sort)
        elif sort == "rewiew":
            query = query.annotate(review_quantity=Count('rewiew')).all()
            return query.order_by('-review_quantity')
        else:
            return query.order_by(f"-{sort}")

    @beartype
    def get_filtered_products_by_category(self, _category_id: str) -> QuerySet[Product]:
        """Получить отфильтрованные по категории продукты"""
        return self.queryset.filter(is_active=True, category_id=int(_category_id))

    @beartype
    def get_filtered_products_by_char(self, _char_id: str) -> QuerySet[Product]:
        """Получить отфильтрованные по Характеристике продукты"""
        return self.queryset.filter(is_active=True,
                                    characteristics__characteristic_value__characteristic_type=int(_char_id))
