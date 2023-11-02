from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    ProductDetailView,
    CatalogListView,
    ComparisonView, AddComparisonView,
    SaleView,
    ProductSaleDetailView,
    ProductGroupSaleDetailView,
    CartSaleDetailView,
    ChangeListProductViewedView, ProductViewedView
)

from core.utils.cache import get_cache_value

urlpatterns = [
    path('comparison/', ComparisonView.as_view(), name="comparison"),
    path('comparison/add/<int:product_id>/', AddComparisonView.as_view(), name="add_comparison"),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name="product"),

    path('changeviewedlist/<int:product_id>', ChangeListProductViewedView.as_view(), name='change_viewed'),
    path('viewed_products/<int:user_id>', ProductViewedView.as_view(), name='viewed_products'),
    path('sale/', SaleView.as_view(), name="sale"),

    path('', CatalogListView.as_view(), name="catalog"),

    path('product_sale/<int:sale_id>/', ProductSaleDetailView.as_view(), name="product_sale_detail"),
    path('group_sale/<int:sale_id>/', ProductGroupSaleDetailView.as_view(), name="product_group_sale_detail"),
    path('cart_sale/<int:sale_id>/', CartSaleDetailView.as_view(), name="cart_sale_detail"),

]
