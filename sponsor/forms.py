from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from sponsor.models import Donations


class DonationForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email_id = forms.EmailField(required=True)
    mobile_no = PhoneNumberField(
                                widget=PhoneNumberPrefixWidget(
                                    initial='GB', #GB works, not UK
                                ),
                                required=True,
                                )
    amount = forms.IntegerField()
    class Meta:
        model = Donations
        fields = ['name', 'email_id','mobile_no','amount']