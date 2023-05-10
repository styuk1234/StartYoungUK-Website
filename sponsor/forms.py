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
        widget=PhoneNumberPrefixWidget(initial="GB"),
        required=True,
    )
    address = forms.CharField(
        label="Full Home Address",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=True,
    )
    is_anonymous = forms.BooleanField(
        label="Make my donation anonymous from public",
        required=False
        )
    is_gift_aid = forms.BooleanField(
        label="Do you want to convert this to a Gift Aid? (for UK Taxpayers only)",
        help_text="By ticking the checkbox above, I declare that I am a UK taxpayer and understand that if I \
            pay less Income Tax and/or Capital Gains Tax in the current tax year than the amount of Gift \
            Aid claimed on all my donations it is my responsibility to pay any difference.",
        required=False
        )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    amount = forms.IntegerField()
    class Meta:
        model = Donation
        fields: list[str] = ["email", "name", "mobile_number", "address", "is_anonymous", "is_gift_aid", "captcha", "amount"]

    def __init__(self, *args, **kwargs):
        super(DonationForm, self).__init__(*args, **kwargs)        
        self.user = kwargs.pop("user", None)
        data = kwargs.pop("instance", None)
        if not isinstance(data, type(None)):
            self.fields["name"].widget.attrs.update({"readonly": "readonly"})
            self.fields["email"].widget.attrs.update({"readonly": "readonly"})
            self.fields["mobile_number"].widget.attrs.update({"readonly": "readonly"})
            self.fields["address"].widget.attrs.update({"readonly": "readonly"})
