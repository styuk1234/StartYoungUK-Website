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
    
    def __init__(self, *args, **kwargs):
        self.user=kwargs.pop('user', None)
        super(DonationForm, self).__init__(*args, **kwargs)
        data = kwargs.pop('instance', None)
        if not isinstance(data, type(None)):
            self.fields['name'].widget.attrs.update({'readonly':'readonly'})
            self.fields['email'].widget.attrs.update({'readonly':'readonly'})
            self.fields['mobile_number'].widget.attrs.update({'readonly':'readonly'})


