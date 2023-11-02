"""Формы приложения Каталог"""
from django import forms

from django.utils.translation import gettext_lazy as _

from .models import Rewiew


class CartEditForm(forms.Form):
    product = forms.CharField(max_length=6)
    product_name = forms.CharField(max_length=250)
    image = forms.CharField(max_length=250)
    count = forms.CharField(max_length=6)
    amount = forms.CharField(max_length=50)
    seller = forms.CharField(max_length=6)

    class Meta:
        fields = ['product', 'product_name', 'image', 'count', 'amount', 'seller']


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""

    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-textarea',
               'id': 'review',
               'name': 'review',
               'placeholder': _('Review')}))

    class Meta:
        model = Rewiew
        fields = [
            'text',
            'user',
            'product'
        ]
