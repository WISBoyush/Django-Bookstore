from django import forms

from .models import Rent


class AddToRentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ()


class MakeRentOrderForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = (
            'city',
            'address',
        )
