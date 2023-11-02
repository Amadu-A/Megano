import datetime
import random
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.cache import cache
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
import inject

from django.views.generic import TemplateView, View, UpdateView

from core.models.cache_setup import CacheSetup
from core.utils.cache import cache_values_list, get_cache_value
from core.utils.injector import configure_inject
from interface.banner_interface import IBanner
from interface.price_interface import IPrice
from interface.product_interface import IProduct
from interface.slider_interface import ISlider

from core.forms import CacheSetupForm

from .utils.cache_key import (
    TOP_PRODUCT_LIST_KEY,
    BANNER_LIST_KEY,
    OFFER_DAY
)


configure_inject()


class PassSuperuserMixin(UserPassesTestMixin):
    """Класс-миксин проверки что текущий пользователь суперюзер"""

    def test_func(self) -> bool | None:
        if self.request.user.is_superuser:
            return True
        return False


class BaseView(TemplateView):
    """Представление отображения блоков контента на главной странице"""
    template_name = 'core/product_supply.html'
    _products: IProduct = inject.attr(IProduct)
    _slider_list: ISlider = inject.attr(ISlider)
    _banner_list: IBanner = inject.attr(IBanner)
    _price_seller: IPrice = inject.attr(IPrice)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offer_day'] = {}
        context['product_top_list'] = cache.get_or_set(TOP_PRODUCT_LIST_KEY,
                                                       self._products.get_product_top_list(const=8),
                                                       get_cache_value('TOP_PRODUCT'))
        context['product_limited_list'] = list(self._products.get_product_limit_list(const=17))
        if context['product_limited_list']:
            context['offer_day'] = cache.get_or_set(OFFER_DAY,
                                                    context['product_limited_list'].pop(random.randint(
                                                        0, len(context['product_limited_list']) - 1)),
                                                    get_cache_value('CATEGORY'))

        context['tomorrow_day'] = (datetime.date.today() + datetime.timedelta(days=2)).strftime('%d.%m.%Y')
        context['slider_list'] = self._slider_list.get_slider_list(const=3)
        context['banner_list'] = cache.get_or_set(BANNER_LIST_KEY,
                                                  self._banner_list.get_banner_list(const=3),
                                                  get_cache_value('BANNER')
                                                  )

        lst = list(context['product_top_list']) + context['product_limited_list']
        if context['offer_day']:
            lst.append(context['offer_day'])
        context['price_seller_list'] = self._price_seller.get_last_minprice_dct(
            _product_id_lst=[i.id for i in lst])

        return context


class AboutView(TemplateView):
    """Представление для отображения информации о маркетплейсе"""
    template_name = 'core/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SetupAdminView(PassSuperuserMixin, View):
    """Страница административных настроек"""
    template_name = 'core/setup-admin.html'
    _SUCCESS_MESSAGE = _('The cache has been cleared')

    def get(self, request, **kwargs):
        """Get"""
        context = {
            'cache_data': cache_values_list(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Post"""
        cache.clear()
        messages.success(self.request, self._SUCCESS_MESSAGE)
        return redirect(self.request.path)


class CacheUpdateView(PassSuperuserMixin, UpdateView):
    """Обновление данных кеша"""
    model = CacheSetup
    form_class = CacheSetupForm
    template_name = 'core/cache_update.html'
    success_url = reverse_lazy('setup-admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key"] = self.object.key
        return context
