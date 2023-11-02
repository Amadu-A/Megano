import inject
from django.utils.translation import gettext as _

from interface.cart_sale_interface import ICartSale
from interface.cartitem_interface import ICartItem
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct


class ProductDiscount:
    _product_sales: IDiscountProduct = inject.attr(IDiscountProduct)
    _product_group_sales: IDiscountProductGroup = inject.attr(IDiscountProductGroup)
    _cart_sales: ICartSale = inject.attr(ICartSale)
    _cart_item: ICartItem = inject.attr(ICartItem)

    def get_all_discount_on_product(self, product_id):
        """
        получать все скидки на товар
        """
        return self._product_sales.get_list_by_id(_id=product_id)

    def get_priority_discount(self, cart_item_qs):
        """
        получить приоритетную скидку на указанный список товаров или на один товар
        """
        try:
            priority = 3
            product_id_qs = cart_item_qs.values('product__id', 'count')
            product_id_lst = [dct['product__id'] for dct in product_id_qs]
        except AttributeError:
            return []
        return_dct = dict()

        dct_group_sales = self._product_group_sales.possible_get_discount(_cart_item_qs=cart_item_qs)
        if dct_group_sales:
            priority = min(dct_group_sales)
            return_dct = dct_group_sales

        dct_cart_sale = self._cart_sales.possible_get_discount(_cart_item_qs=cart_item_qs)
        if dct_cart_sale and priority > dct_cart_sale.priority:
            priority = dct_cart_sale.priority
            return_dct = {dct_cart_sale.priority: {}}
            for product_id in product_id_lst:
                return_dct[dct_cart_sale.priority][product_id] = [dct_cart_sale, [True, _(
                    'Discount on the shopping cart has been applied! Benefit ') + str(dct_cart_sale.value) + ' %']]

        dct_product_sale = dict()
        for product_id in product_id_lst:
            sales = self.get_all_discount_on_product(product_id)
            if sales:
                sale = sales.order_by('-value').first()
                dct_product_sale[sale.priority] = dct_product_sale.get(sale.priority, {product_id: sale})
                dct_product_sale[sale.priority][product_id] = [sale, [True, _(
                    'The discount on the product has been applied! Benefit ') + str(sale.value) + ' %']]
        if dct_product_sale and priority >= min(dct_product_sale):
            priority = min(dct_product_sale)
            for product_id in product_id_lst:
                dct_product_sale[priority][product_id] = dct_product_sale[priority].get(product_id, [None, [False, '']])
            return_dct = dct_product_sale

        new_return_lst = []
        if return_dct:
            for key, value in list(return_dct.values())[0].items():
                dct = dict()
                dct['product_id'] = key
                dct['sale_model'] = value[0]
                dct['message'] = ''
                dct['discount'] = False
                dct['count'] = 1
                if value[0]:
                    dct['message'] = value[1][-1]
                    dct['discount'] = value[1][-2]
                    try:
                        if value[-1].get('count', None):
                            dct['count'] = value[-1]['count']
                    except AttributeError:
                        pass
                new_return_lst.append(dct)

        return new_return_lst

    def calculate_price_with_discount(self, cart_item_qs):
        """
        рассчитать цену со скидкой на товар
        """
        return_lst = self.get_priority_discount(cart_item_qs)
        sale_instances_tpl = ((dct['sale_model'], dct['count']) for dct in return_lst)
        sale_instances_count = dict()
        for sale in sale_instances_tpl:
            if not sale_instances_count.get(sale[0], None):
                sale_instances_count[sale[0]] = sale[1]
            if sale_instances_count[sale[0]] > sale[1]:
                sale_instances_count[sale[0]] = sale[1]

        for key, sale_dct in enumerate(return_lst):
            for sale_instance, count in sale_instances_count.items():
                if sale_instance == sale_dct['sale_model']:
                    sale_dct['count'] = count
                    return_lst[key]['count'] = count

            for item in cart_item_qs:
                sale = 0
                if item.product.id == sale_dct['product_id']:
                    return_lst[key]['amount'] = item.amount
                    if (sale_dct['sale_model'] and sale_dct['discount']) and sale_dct['sale_model'].value:
                        sale = item.amount * sale_dct['sale_model'].value / 100
                        return_lst[key]['sale_amount'] = item.amount - sale
                    elif (sale_dct['sale_model'] and sale_dct['discount']) and sale_dct['sale_model'].amount:
                        sale = sale_dct['sale_model'].amount / len(
                            sale_dct['sale_model'].category.all()) * sale_dct['count']
                        return_lst[key]['sale_amount'] = item.amount - sale
                        if sale_dct['sale_model'] and (
                                (sale_dct['sale_model'].fixprice * sale_dct['count']) > (item.amount - sale)):
                            sale = item.amount / item.count * sale_dct['count'] - sale_dct['sale_model']\
                                .fixprice * sale_dct['count']
                            return_lst[key]['sale_amount'] = sale_dct['sale_model'].fixprice * sale_dct['count']
                    self._cart_item.update(_cart_item=item, _sale=sale)

        if not return_lst and cart_item_qs:
            for item in cart_item_qs:
                sale = 0
                self._cart_item.update(_cart_item=item, _sale=sale)

        return return_lst
