from django.urls import path
from django.views.decorators.cache import never_cache

from .views import CartListView, ChangeCountProductView, DeleteCartItemView, AddProductToCartView

app_name = 'cart_app'

urlpatterns = [
    path('', never_cache(CartListView.as_view()), name="cart"),
    path('change', never_cache(ChangeCountProductView.as_view()), name="change_count"),
    path('delete', DeleteCartItemView.as_view(), name="item_delete"),
    path('add', AddProductToCartView.as_view(), name="catalog_add"),
]
