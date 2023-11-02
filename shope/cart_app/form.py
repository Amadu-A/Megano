from django import forms


class ChangeCountForm(forms.Form):
    product = forms.CharField(max_length=8)
    count = forms.CharField(max_length=8)
    seller = forms.CharField(max_length=8)

    class Meta:
        fields = ['product', 'count', 'seller']


class DeleteForm(forms.Form):
    product = forms.CharField(max_length=8)

    class Meta:
        fields = ['product']


class CartEditForm(forms.Form):
    product = forms.CharField(max_length=6)
    product_name = forms.CharField(max_length=250)
    image = forms.CharField(max_length=250)
    count = forms.CharField(max_length=6)
    amount = forms.CharField(max_length=50)
    seller = forms.CharField(max_length=6)

    class Meta:
        fields = ['product', 'product_name', 'image', 'count', 'amount', 'seller']

