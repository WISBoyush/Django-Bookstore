from django import forms

from cart.models import Purchase


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ()
