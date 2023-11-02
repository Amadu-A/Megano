"""Pay app urls"""

from django.urls import path
from .views import CreatePaymentView, SuccessPaymentView, SuccessApiView


app_name = 'pay_app'

urlpatterns = [
    path('new-pay/<int:pk>/', CreatePaymentView.as_view(), name='new-pay'),
    path('success-pay/<int:pk>', SuccessPaymentView.as_view(), name='success-pay'),
    path('success-api/', SuccessApiView.as_view(), name='success-api'),

]
