from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from sponsor.models import Donation


class DonationForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    mobile_number = PhoneNumberField(
                                widget=PhoneNumberPrefixWidget(
                                    initial='GB'
                                ),
                                required=True,
                                )
    amount = forms.IntegerField()
    class Meta:
        model = Donation
        fields = ['name', 'email','mobile_number', 'amount']