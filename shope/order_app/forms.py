"""Forms for order app"""

from django import forms
from django.utils.translation import gettext_lazy as _
from order_app.models import Order
from core.enums import PayType, DeliveryType, OrderStatus


class CreateOrderForm(forms.ModelForm):
    """Форма создания заказа"""

    city = forms.CharField(label=_('City'),
                           widget=forms.TextInput(
                               attrs={'class': 'form-input',
                                      'id': 'city',
                                      'name': 'city',
                                      'data-validate': 'require'}))

    address = forms.CharField(label=_('Address'),
                              widget=forms.Textarea(
                                  attrs={'class': 'form-textarea',
                                         'id': 'address',
                                         'name': 'address',
                                         'data-validate': 'require'}))

    delivery_type = forms.CharField(label=_('Delivery type'),
                                    required=False,
                                    widget=forms.RadioSelect(choices=DeliveryType.choices,
                                                             attrs={'class': 'toggle-box',
                                                                    'onchange': 'deliveryChange(this);',
                                                                    }))

    pay_type = forms.CharField(label=_('Pay type'),
                               required=False,
                               widget=forms.RadioSelect(choices=PayType.choices,
                                                        attrs={'class': 'toggle-box',
                                                               'onchange': 'payChange(this);',
                                                               }))

    class Meta:
        """Meta Class"""
        model = Order
        fields = [
            'city',
            'address',
            'delivery_type',
            'pay_type',
            'user',
            'amount'
        ]
