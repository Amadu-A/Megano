"""Order views"""

from decimal import Decimal
from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
import inject
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from core.utils.injector import configure_inject
from interface.order_interface import IOrder
from interface.order_item_interface import IOrderItem
from interface.cart_interface import ICart
from order_app.models import Order, OrderItem
from profile_app.forms import EditProfileForm, EditUserForm
from order_app.forms import CreateOrderForm
from core.utils.cache import get_cache_value
from core.enums import DeliveryType
from .utils import CartMixin


configure_inject()


class EmptyCart(TemplateView):
    template_name = 'order_app/empty-cart.html'


class HistoryOrderView(LoginRequiredMixin, ListView):
    """Oreder list tempale class. Will be deleted"""
    template_name = 'order_app/historyorder.html'
    context_object_name = 'order_list'
    paginate_by = 3
    model = Order
    _order_list: IOrder = inject.attr(IOrder)

    def get_queryset(self):
        return self._order_list.get_list_by_user(self.request.user)  # type: ignore


class DetailOrderView(DetailView):
    """Детальная страница заказа"""
    template_name = 'order_app/oneorder.html'
    model = Order
    context_object_name = 'order'
    _order: IOrder = inject.attr(IOrder)
    _order_item = inject.attr(IOrderItem)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self._order_item.get_by_order(self.get_object())  # type: ignore
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        return redirect('pay_app:new-pay', self.kwargs.get('pk'))


class CreateOrderView(LoginRequiredMixin, CartMixin, CreateView):
    """Создание заказа"""
    template_name = 'order_app/order.html'
    context_object_name = 'order'
    form_class = CreateOrderForm
    model = Order
    _cart = inject.attr(ICart)
    _order_items = inject.attr(IOrderItem)

    def get_success_url(self) -> str:
        """get success url"""
        return reverse('order_app:history-order')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart = self._cart.get_active_by_user(self.request.user)
        context['cart'] = cart
        context['user_form'] = EditUserForm(instance=self.request.user)
        context['profile_form'] = EditProfileForm(instance=self.request.user.profile)  # type: ignore
        context['total_amount'] = self._cart.total_amount(cart)

        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = CreateOrderForm(self.request.POST)  # type: ignore
        user_form = EditUserForm(self.request.POST,
                                 instance=request.user)
        profile_form = EditProfileForm(self.request.POST,
                                       instance=request.user.profile)  # type: ignore
        cart = self._cart.get_active_by_user(request.user)

        valid_list = [form.is_valid(), user_form.is_valid(), profile_form.is_valid()]

        if all(valid_list):
            order_obj = form.save()
            user_form.save()
            profile_form.save()
            cart.is_active = False
            self._cart.save(cart)
            cart_list = self._cart.model_to_list(cart)
            bulk_list = [OrderItem(order=order_obj, **i_cart_list) for i_cart_list in cart_list]
            for item in bulk_list:
                product = item.product
                product.number_of_sales += 1
                product.save()
            self._order_items.bulk_create(bulk_list)

            return redirect('pay_app:new-pay', order_obj.pk)
        else:
            cart = self._cart.get_active_by_user(request.user)
            context = {
                'cart': cart,
                'total_amount': self._cart.total_amount(cart),
                'form': form,
                'user_form': user_form,
                'profile_form': profile_form
            }

        return render(request, self.template_name, context=context)


class DeliveryTypeView(View):
    """Изменение способа доставки"""
    _cart = inject.attr(ICart)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any):

        delivery_type = request.POST['delivery_type']
        min_amount = get_cache_value('MIN_AMOUNT_FOR_FREE_DELIVERY')
        cost_delivery = get_cache_value('COST_DELIVERY')

        cart = self._cart.get_active_by_user(self.request.user)
        total_amount = self._cart.total_amount(cart)
        if total_amount < min_amount and delivery_type == DeliveryType.EXPRESS.name:
            total_amount = total_amount + cost_delivery

        else:
            cost_delivery = 0

        response = {
            'total_amount': total_amount,
            'cost_delivery': cost_delivery,
        }

        return JsonResponse(data=response, status=201)
