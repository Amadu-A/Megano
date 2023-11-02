import json
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from rest_framework.views import APIView
from rest_framework.response import Response
from core.utils.payment import OrderPayment

from order_app.models import Order
import inject
from interface.order_interface import IOrder


class CreatePaymentView(View):
    """Оплатить заказ"""
    template_name = 'pay_app/new_payment.html'

    def get(self, request, pk):
        context = {'confirmation_t': OrderPayment().new_order_pay(pk),
                   'pk': pk}

        return render(request, self.template_name, context)


class SuccessPaymentView(View):
    """Успешная оплата заказа."""

    def get(self, request, pk):
        OrderPayment().pay_notifications(pk)
        return redirect('order_app:one-order', pk)


class SuccessApiView(APIView):
    """Получить уведомление о платеже с yookassa API"""

    def post(self, request):
        """post"""

        if OrderPayment().pay_api_notifications(request.data):
            return Response(status=200)

        else:
            return Response(status=404)
