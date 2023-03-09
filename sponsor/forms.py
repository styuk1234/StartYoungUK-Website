from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from sponsor.models import Donation
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class DonationForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    mobile_number = PhoneNumberField(
                                widget=PhoneNumberPrefixWidget(
                                    initial='GB'
                                ),
                                required=True,
                                )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    amount = forms.IntegerField()
    
    class Meta:
        model = Donation
        fields = ['email', 'name', 'mobile_number', 'captcha', 'amount']