from django import forms
from django.contrib.auth.models import User
from django_countries.fields import CountryField


PAYMENT_CHOICES = (("C", "Credit Card"), ("P", "PayPal"))


class CheckoutForm(forms.Form):

    email = forms.EmailField()
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "First Name"})
    )
    last_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Last Name"})
    )
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Address"}))
    country = CountryField(blank_label="(select country)").formfield()
    zip_code = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Zip Code"})
    )
    phone = forms.IntegerField()
    payment_options = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES
    )
    ship_to_address = forms.BooleanField(widget=forms.CheckboxInput())
    shipping_order = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Notes about your order, Special Notes for Delivery",
                "rows": 16,
            }
        )
    )

