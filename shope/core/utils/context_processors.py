from django.core.cache import cache
from django.conf import settings
from core.utils.cache import get_cache_value

from core.utils.add_product_to_cart import AddProductToCart
from catalog_app.models import Category

from .cache_key import (
    CATEGORY_LIST_KEY,
)


def cart_processor(request):

    if request.user.is_authenticated:

        amount, count, discount = AddProductToCart().get_count_product_in_cart(user=request.user)
        return {'amount': amount, 'count': count, 'discount': discount}

    else:

        amount, count, discount = AddProductToCart().get_count_product_for_anonymous_user(request)
        return {'amount': amount, 'count': count, 'discount': discount}


def get_category_list(request):

    cat_lst = cache.get_or_set(
        CATEGORY_LIST_KEY,
        Category.objects.all().prefetch_related('characteristictype_set'),
        get_cache_value('CATEGORY')
    )

    return {'category_list': cat_lst}
