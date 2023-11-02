"""Catalog app views"""

from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.shortcuts import redirect, render

from django.core.cache import cache
import inject

from django.http import HttpResponseRedirect
from django.views import View

from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import TemplateView, ListView, DetailView

from core.utils.injector import configure_inject
from interface.cart_sale_interface import ICartSale
from interface.category_interface import ICategory
from interface.compare_product_interface import ICompareProduct
from interface.price_interface import IPrice
from interface.product_interface import IProduct
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct

from interface.characteristic_interface import ICharacteristicProduct
from catalog_app.models import DiscountProduct, DiscountProductGroup, CartSale
from catalog_app.models import Product

from interface.product_viewed_interface import IProductViewed

from interface.catalog_filter_interface import ICatalogFilter
from interface.seller_interface import ISeller
from interface.review_interface import IReview

from catalog_app.form import ReviewForm
from core.utils.cache import get_cache_value

from core.utils.cache_key import (
    DETAIL_PRODUCT_KEY,
    PRODUCTS_KEY,
    CATALOG_CATEGORY,
)

configure_inject()


class ProductDetailView(DetailView):
    """Детальная страница продукта"""
    _characteristics: ICharacteristicProduct = inject.attr(ICharacteristicProduct)
    _sellers_of_product: IProduct = inject.attr(IProduct)
    _price_of_seller: ISeller = inject.attr(ISeller)
    _review: IReview = inject.attr(IReview)

    model = Product
    template_name = 'catalog_app/product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_queryset(self):
        """get querysert"""
        key = PRODUCTS_KEY
        qs = cache.get(key)
        if not qs:
            qs = Product.objects.all()
            cache.set(key, qs, get_cache_value('DETAIL_PRODUCT'))
        return qs

    def get_context_data(self, **kwargs):
        """get_context_data"""
        key = DETAIL_PRODUCT_KEY + str(self.kwargs['product_id'])
        cache_time = get_cache_value('DETAIL_PRODUCT')

        context = cache.get(key)

        if not context:
            context = {}
            context = super().get_context_data(**kwargs)
            context['characteristics'] = self._characteristics.get_by_product(_product=self.object)
            context['reviews'] = self._review.get_by_product(self.kwargs['product_id'])
            sellers = []
            min_price = {'price': 0,
                         'seller': None}
            qs_sellers = self._sellers_of_product.get_sellers_of_product(self.kwargs['product_id'])

            for i_seller in qs_sellers:
                price = self._price_of_seller.get_last_price_of_product(
                    i_seller['price__seller'],
                    self.kwargs['product_id']
                )
                sellers.append(price)
                if (price['product_seller__price'] < min_price['price']) or min_price['price'] == 0:
                    min_price['price'] = price['product_seller__price']
                    min_price['seller'] = price['pk']

            context['sellers'] = sellers
            context['min_price'] = min_price

            cache.set(key, context, cache_time)

        context['review_form'] = ReviewForm()
        context['cache_time'] = cache_time
        return context

    def post(self, request, product_id):
        """Метод post для добавление отзыва"""
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form.save()
            return redirect(self.request.path)

        context = {
            'review_form': review_form,
        }

        return render(request, self.template_name, context=context)


class CatalogListView(ListView):
    """Каталог"""
    template_name = 'catalog_app/catalog.html'
    _filter: ICatalogFilter = inject.attr(ICatalogFilter)
    _price_seller: IPrice = inject.attr(IPrice)
    paginate_by = 9

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset().values('id')

        context['price_seller_list'] = self._price_seller.get_last_minprice_dct(
            _product_id_lst=qs)

        return context

    def get_queryset(self):
        try:
            global query
            if self.request.GET.get('category') is not None:
                category_id = self.request.GET.get('category')
                query = cache.get_or_set(CATALOG_CATEGORY + str(category_id),
                                         self._filter.get_filtered_products_by_category(category_id),
                                         get_cache_value('CATEGORY')
                                         )
            elif self.request.GET.get('char') is not None:
                char_id = self.request.GET.get('char')
                query = self._filter.get_filtered_products_by_char(char_id)
            elif self.request.GET.get('tag') is not None:
                tag_name = self.request.GET.get('tag')
                query = self._filter.filter_by_tag(tag_name)
            elif self.request.GET.get('sort') is not None:
                sort = self.request.GET.get('sort')
                return self._filter.filter_by_sort(sort, query)
            else:
                is_limited = True if self.request.GET.get('in_stock') else False
                free_delivery = True if self.request.GET.get('free_delivery') else False
                if self.request.GET.get('price'):
                    product_min_price, product_max_price = self.request.GET.get('price').split(';')
                else:
                    product_min_price, product_max_price = None, None
                product_name = self.request.GET.get('title')

                qs = self._filter.get_filtered_products(product_name=product_name,
                                                        free_delivery=free_delivery,
                                                        is_limited=is_limited,
                                                        product_min_price=product_min_price,
                                                        product_max_price=product_max_price)

                if (product_name is None and free_delivery is None and is_limited is
                        None and product_min_price is None and product_max_price is None):
                    query = cache.get_or_set(CATALOG_CATEGORY, qs, get_cache_value('CATEGORY'))
                else:
                    query = qs

            return query

        except MultiValueDictKeyError:
            return Product.objects.prefetch_related('image', 'tag')


class ComparisonView(TemplateView):
    """Представление для просмотра характеристик товаров, сравнения их с другими товарами со схожими характеристиками"""
    template_name = 'catalog_app/comparison.html'
    _compare_product: ICompareProduct = inject.attr(ICompareProduct)
    _price_seller: IPrice = inject.attr(IPrice)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.save()
            session_key = self.request.session.session_key
        context['compare_list'] = self._compare_product.get_compare_product_list(_session_key=session_key)
        context['price_seller_list'] = self._price_seller.get_last_minprice_dct(
            _product_id_lst=[i.product.id for i in context['compare_list']])
        return context

    def post(self, request, *args, **kwargs):
        session_key = self.request.session.session_key
        self._compare_product.delete_compare_product_by_id(
            _session_key=session_key,
            _compare_product_id=int(request.POST.get('compare_id'))
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddComparisonView(View):
    """Представление для обработки удаления, добавления и контроля количества просмотренных товаров"""
    _compare_product: ICompareProduct = inject.attr(ICompareProduct)

    def post(self, request, *args, **kwargs):
        return_dict = dict()
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        product_id = kwargs.get('product_id')
        return_dict['session_key'] = session_key
        return_dict['product_id'] = product_id
        compare_list = self._compare_product.get_compare_product_list(_session_key=session_key)
        if len(compare_list) > 1:
            return_dict['message'] = _("Too much products to the comparison!")
            return JsonResponse(return_dict)
        if compare_list and compare_list[0].product.id == product_id:
            return_dict['message'] = _("The product was already added!")
            return JsonResponse(return_dict)
        if self._compare_product.get_compare_product_list(_session_key=session_key) and \
                not self._compare_product.possible_compare_product(_product_id=product_id, _session_key=session_key):
            return_dict['message'] = _("The product have no common characteristics!")
            return JsonResponse(return_dict)
        self._compare_product.create_compare_product(_product_id=product_id, _session_key=session_key)
        return_dict['message'] = _("The product has been added to the comparison!")
        return JsonResponse(return_dict)


class SaleView(ListView):
    """Представление для просмотра списка скидок"""
    template_name = 'catalog_app/sale.html'
    _product_sales: IDiscountProduct = inject.attr(IDiscountProduct)
    _product_group_sales: IDiscountProductGroup = inject.attr(IDiscountProductGroup)
    _cart_sales: ICartSale = inject.attr(ICartSale)
    context_object_name = 'sales'

    def get_queryset(self):
        queryset = {'product_sales': self._product_sales.get_list(),
                    'product_group_sales': self._product_group_sales.get_list(),
                    'cart_sales': self._cart_sales.get_list(),
                    }
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductSaleDetailView(DetailView):
    """Представление для просмотра детализированной информации по скидке на товар или категорию товаров"""
    template_name = 'catalog_app/sale_detail.html'
    model = DiscountProduct
    context_object_name = 'sale'
    pk_url_kwarg = 'sale_id'


class ProductGroupSaleDetailView(DetailView):
    """Представление для просмотра детализированной информации по скидке на группы товаров"""
    template_name = 'catalog_app/sale_detail.html'
    model = DiscountProductGroup
    context_object_name = 'sale'
    pk_url_kwarg = 'sale_id'


class CartSaleDetailView(DetailView):
    """Представление для просмотра детализированной информации по скидке на корзину"""
    template_name = 'catalog_app/sale_detail.html'
    model = CartSale
    context_object_name = 'sale'
    pk_url_kwarg = 'sale_id'


class ChangeListProductViewedView(View):
    """Представление для изменения списка просмотренных товаров"""
    _product_viewed_list: IProductViewed = inject.attr(IProductViewed)
    _create_product_viewed: IProductViewed = inject.attr(IProductViewed)
    _get_product_viewed_by_id: IProductViewed = inject.attr(IProductViewed)
    _delete_product_viewed_by_id: IProductViewed = inject.attr(IProductViewed)

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        if request.user.is_authenticated:
            user_id = request.user.id
            product = self._get_product_viewed_by_id.get_product_viewed_by_id(_user_id=user_id, _product_id=product_id)
            if not product:
                self._create_product_viewed.create_product_viewed(_user_id=user_id, _product_id=product_id)
            else:
                self._delete_product_viewed_by_id.delete_product_viewed_by_id(_user_id=user_id, _product_id=product_id)
                self._create_product_viewed.create_product_viewed(_user_id=user_id, _product_id=product_id)
            product_viewed_list = self._product_viewed_list.get_product_viewed_list(_user_id=user_id)
            if len(product_viewed_list) > 20:
                self._delete_product_viewed_by_id.delete_product_viewed_by_id(
                    _user_id=product_viewed_list.first().user_id, _product_id=product_viewed_list.first().product_id)
        return HttpResponseRedirect(f'/catalog/product/{product_id}/')


class ProductViewedView(ListView):
    """Представление для отображения списка просмотренных товаров"""
    template_name = 'catalog_app/product_viewed.html'
    _category_list: ICategory = inject.attr(ICategory)
    _product_viewed_list: IProductViewed = inject.attr(IProductViewed)
    paginate_by = 8

    def get_queryset(self):
        return self._product_viewed_list.get_product_viewed_list(_user_id=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['product_viewed_list'] = self._product_viewed_list.get_product_viewed_list(_user_id=user_id)
        context['category_list'] = self._category_list.get_category_list()
        return context
