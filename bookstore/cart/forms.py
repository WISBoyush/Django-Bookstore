from django import forms

from cart.models import Purchase

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'choose-quantity',
        'value': '1'}
    ), min_value=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartDeleteItemForm(forms.Form):
    model = Purchase


class OrderForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = (
            'city',
            'address')
