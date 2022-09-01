from django import forms

from cart.models import Purchase

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartDeleteItemForm(forms.Form):
    model = Purchase


class OrderForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = (
            'city',
            'address')
