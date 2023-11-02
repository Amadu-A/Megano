"""Forms for order app"""

from django import forms
from django.utils.translation import gettext_lazy as _
from core.models.cache_setup import CacheSetup


class CacheSetupForm(forms.ModelForm):
    """Форма  настроек кеша"""

    value = forms.IntegerField(label=_('Value'),
                               widget=forms.NumberInput(
                               attrs={'class': 'form-input',
                                      'data-validate': 'require'}))

    class Meta:
        """Meta Class"""
        model = CacheSetup
        fields = [
            'value',
        ]
