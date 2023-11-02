from typing import Optional

from beartype import beartype
from beartype.typing import Dict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.utils.translation import gettext as _
from django.db.models import DateTimeField
from django.db.models.functions import Cast
from django.utils import timezone

from catalog_app.models import DiscountProductGroup, Category
from interface.discount_product_group_interface import IDiscountProductGroup


today = Cast(timezone.now().date(), output_field=DateTimeField())


class DiscountProductGroupRepository(IDiscountProductGroup):

    @beartype
    def get_list(self) -> QuerySet[DiscountProductGroup]:
        """Вернуть кверисет скидок на продукт"""
        return DiscountProductGroup.objects.all()

    @beartype
    def possible_get_discount(self, _cart_item_qs: QuerySet) -> Optional[Dict]:
        """Вернуть возможность применения скидки"""
        cat_id_qs = _cart_item_qs.values('product__category__id')
        cat_id_lst = [dct['product__category__id'] for dct in cat_id_qs]
        qs_cats = Category.objects.filter(
            discountproductgroup__category__in=cat_id_lst,
            discountproductgroup__data_end__gte=today,
            discountproductgroup__data_start__lte=today
        )
        qs = qs_cats.filter(id__in=cat_id_lst).distinct()
        dct = dict()
        flag = False
        for cat in qs:
            sale = DiscountProductGroup.objects.get(category__id=cat.id)
            if sale:
                dct[sale.priority] = dct.get(sale.priority, {sale._meta.model_name: {sale.id: 0}})
                if not dct[sale.priority][sale._meta.model_name].get(sale.id, None):
                    dct[sale.priority][sale._meta.model_name] = {sale.id: 0}
                dct[sale.priority][sale._meta.model_name][sale.id] += 1
                if dct[sale.priority][sale._meta.model_name][sale.id] > 1:
                    flag = True
        new_dct = {}
        if flag:
            product_id_qs = _cart_item_qs.values('product__id', 'count')
            product_id_cnt_lst = [(dct_prod['product__id'], dct_prod['count']) for dct_prod in product_id_qs]
            priority = min(list(dct.keys()))
            new_dct[priority] = {}
            for product_id, count in product_id_cnt_lst:
                try:
                    sale_object = DiscountProductGroup.objects.get(category__product__id=product_id)
                except ObjectDoesNotExist:
                    sale_object = None
                new_dct[priority][product_id] = [sale_object]
                if sale_object:
                    new_dct[priority][product_id] = [sale_object, list(sale_object.category.all())]
                    for cat in list(sale_object.category.all()):
                        for cat_id in cat_id_lst:
                            if cat.id == cat_id:
                                index = new_dct[priority][product_id][1].index(cat)
                                new_dct[priority][product_id][1][index] = False
                                break
                    if all([type(x) is bool for x in new_dct[priority][product_id][1]]):
                        new_dct[priority][product_id][1].append(True)
                        new_dct[priority][product_id][1].append(_('Discount successfully applied'))
                        new_dct[priority][product_id].append({'count': count})
                    else:
                        message_cat = '/'
                        for cat in new_dct[priority][product_id][1]:
                            if cat:
                                message_cat = message_cat + cat.title + '/'
                        new_dct[priority][product_id][1].append(False)
                        new_dct[priority][product_id][1].append(
                            _('To get a discount, add an item from the category ') + str(message_cat))
            return new_dct
        return None
