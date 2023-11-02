"""Order app urls"""

from django.urls import path
from .views import (HistoryOrderView,
                    DetailOrderView,
                    CreateOrderView,
                    EmptyCart,
                    DeliveryTypeView)


app_name = 'order_app'

urlpatterns = [
    path('history-order/', HistoryOrderView.as_view(), name='history-order'),
    path('empty-cart/', EmptyCart.as_view(), name='empty-cart'),
    path('one-order/<int:pk>/', DetailOrderView.as_view(), name='one-order'),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('delivery-type/', DeliveryTypeView.as_view(), name='delivery-type')
]
