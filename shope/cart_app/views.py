from django.http import JsonResponse, HttpRequest
from django.template.loader import render_to_string
from django.views.generic import ListView, TemplateView

from core.utils.product_discount import ProductDiscount
from .form import ChangeCountForm, DeleteForm, CartEditForm
from core.utils.add_product_to_cart import AddProductToCart

from django.utils.translation import gettext as _


class CartListView(ListView):
    template_name = 'cart_app/cart.html'
    context_object_name = "items"

    def get_queryset(self):
        return AddProductToCart().get_list_in_cart(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['discount_data'] = ProductDiscount().calculate_price_with_discount(cart_item_qs=self.get_queryset())
        return context


class ChangeCountProductView(TemplateView):
    add_product_to_cart = AddProductToCart()

    def post(self, request):
        if request.headers['X-Requested-With'] == 'XMLHttpRequest':

            form = ChangeCountForm(request.POST)

            if form.is_valid():
                if request.user.is_authenticated:
                    product_amount = self.add_product_to_cart.change_count_product_in_cart(request.user,
                                                                                           **form.cleaned_data)
                else:
                    product_amount = self.add_product_to_cart.change_count_for_anonymous(request, **form.cleaned_data)

                cart_edit = render_to_string('includes/card_edit.html',
                                             request=request)
                discount_data = ProductDiscount().calculate_price_with_discount(
                    cart_item_qs=self.add_product_to_cart.get_list_in_cart(request))
                count_change = render_to_string('includes/price_product_in_cart.html',
                                                context={'item': product_amount, 'discount_data': discount_data},
                                                request=request)

                total_amount = render_to_string(
                    'includes/total_amount_in_cart.html',
                    request=request,
                    context={'discount_data': discount_data}
                )

                qs = self.add_product_to_cart.get_list_in_cart(request)
                new_qs = render_to_string('includes/product-in-cart.html',
                                          context={'items': qs,
                                                   'discount_data': discount_data},
                                          request=request)

                return JsonResponse({'cart': cart_edit,
                                     'new_qs': new_qs,
                                     'total_amount': total_amount})


class AddProductToCartView(TemplateView):
    add_product_to_cart = AddProductToCart()

    def post(self, request: HttpRequest):
        if request.headers['X-Requested-With'] == 'XMLHttpRequest':
            form = CartEditForm(data=request.POST)
            if form.is_valid():
                if request.POST['count'] == '0':
                    message = _('Select the number of products')
                    return JsonResponse({'message': message})

                if request.user.is_authenticated:
                    self.add_product_to_cart.add_product_to_cart(request.user, **form.cleaned_data)
                else:
                    self.add_product_to_cart.add_product_for_anonymous_user(request, **form.cleaned_data)

                message = _('The product has been added to the cart')

                result = render_to_string('includes/card_edit.html', request=request)

                return JsonResponse({'result': result, 'message': message})

            else:
                message_error = _("Something went wrong")
                return JsonResponse({'message': message_error})


class DeleteCartItemView(TemplateView):
    add_product_to_cart = AddProductToCart()

    def post(self, request):
        form = DeleteForm(request.POST)

        if form.is_valid():
            self.add_product_to_cart.remove_product_from_cart(form.cleaned_data['product'], self.request)

            cart_edit = render_to_string('includes/card_edit.html',
                                         request=request)

            total_amount = render_to_string('includes/total_amount_in_cart.html',
                                            request=request)

            discount_data = ProductDiscount().calculate_price_with_discount(
                cart_item_qs=self.add_product_to_cart.get_list_in_cart(request))
            qs = self.add_product_to_cart.get_list_in_cart(request)
            new_qs = render_to_string('includes/product-in-cart.html',
                                      context={'items': qs,
                                               'discount_data': discount_data},
                                      request=request)

            return JsonResponse({'cart': cart_edit,
                                 'total_amount': total_amount,
                                 'new_qs': new_qs})
