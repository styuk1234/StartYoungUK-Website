from math import fabs
import re
from xml.dom import ValidationErr
from xmlrpc.client import Boolean
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from users.models import StartYoungUKUser
from django.core.validators import MinLengthValidator
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class UserRegisterForm(UserCreationForm):
    display_name = forms.CharField(required=True)
    user_type = forms.ChoiceField(choices=(('I', 'Individual'), ('C', 'Corporate')), required=True)
    email = forms.EmailField(required=True)
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
            initial='GB',  # GB works, not UK
        ),
        required=True,
    )
    address = forms.CharField(
        widget=forms.Textarea(),
        required=True,
    )
    crn_no = forms.CharField(
        label="Company Registration Number (CRN)",
        required=False,
        help_text="If you're signing up as a corporate, please enter your CRN",
        validators=[MinLengthValidator(limit_value=8)],
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ['display_name', 'user_type', 'email', 'phone_number', 'address', 'crn_no', 'username', 'password1',
                  'password2', 'captcha']

    def clean_email(self):
        # Validate unique email
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError('This email is already registered.')

    def clean_phone_number(self):
        # Validate unique phone_number
        phone_number = self.cleaned_data["phone_number"]

        try:
            StartYoungUKUser.objects.get(phone_number=phone_number)

        except StartYoungUKUser.DoesNotExist:

            return phone_number

        raise forms.ValidationError("This Phone Number is already registered.")

    def clean_crn_no(self):
        # Validate unique CRN
        crn_no = self.cleaned_data["crn_no"]
        user_type = self.cleaned_data["user_type"]

        try:
            # Check if CRN exists and is non-default
            StartYoungUKUser.objects.get(crn_no=crn_no) and crn_no != ""
            if user_type == 'C' and not crn_no:
                # If user is corporate type but has not entered CRN, prompt validation error
                print("in except 1")
                raise ValidationError(
                    "Since you've chosen corporate user, please enter your CRN for validation."
                )
            elif user_type == 'I':
                # Individual user might have put something by mistake in CRN field, so just get rid of it
                # when entering it into the database
                self.cleaned_data['crn_no'] = '00000000'
                print("in except 2")
                return "00000000"

        except StartYoungUKUser.DoesNotExist:
            return crn_no

        raise forms.ValidationError("This CRN is already registered.")


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class MentorRegistrationForm(forms.Form):
    painting=forms.BooleanField(required=False)
    football=forms.BooleanField(required=False)
    reading=forms.BooleanField(required=False)
    dancing=forms.BooleanField(required=False)
    singing=forms.BooleanField(required=False)
    cooking=forms.BooleanField(required=False)
    cricket=forms.BooleanField(required=False)
    arts_and_crafts=forms.BooleanField(required=False)
    adventure=forms.BooleanField(required=False)
    writing=forms.BooleanField(required=False)
    occupation=forms.CharField(max_length=20)

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['display_name', 'user_type', 'email', 'phone_number', 'address', 'crn_no', 'captcha']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateUserForm, self).__init__(*args, **kwargs)

    display_name = forms.CharField(required=True)
    user_type = forms.ChoiceField(choices=(('I', 'Individual'), ('C', 'Corporate')), required=True)

    # email = forms.EmailField(required=True)
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
            initial='GB',  # GB works, not UK
        ),
        required=True,
    )
    address = forms.CharField(
        widget=forms.Textarea(),
        required=True,
    )
    crn_no = forms.CharField(
        label="Company Registration Number (CRN)",
        required=False,
        help_text="If you're signing up as a corporate, please enter your CRN",
        validators=[MinLengthValidator(limit_value=8)],
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean_email(self):
        # Validate unique email

        email = self.cleaned_data["email"]
        username = self.cleaned_data.get('username')
        if User.objects.filter(email__iexact=email).count() > 1:
            raise forms.ValidationError('This email address is already in use. '
                                        'Please supply a different email address.')
        else:
            return email

    def clean_phone_number(self):
        # Validate unique phone_number
        phone_number = self.cleaned_data["phone_number"]

        try:
            #   StartYoungUKUser.objects.get(phone_number=phone_number)
            StartYoungUKUser.objects.filter(phone_number=phone_number).exclude(
                phone_number=self.cleaned_data["phone_number"])
        except StartYoungUKUser.DoesNotExist:

            return phone_number

        raise forms.ValidationError("This Phone Number is already registered.")

    def clean_crn_no(self):
        # Validate unique CRN
        crn_no = self.cleaned_data["crn_no"]
        user_type = self.cleaned_data["user_type"]

        try:
            # Check if CRN exists and is non-default
            StartYoungUKUser.objects.get(crn_no=crn_no) and bool(crn_no)

        except StartYoungUKUser.DoesNotExist:
            if user_type == 'C' and not crn_no:
                # If user is corporate type but has not entered CRN, prompt validation error
                raise ValidationError(
                    "Since you've chosen corporate user, please enter your CRN for validation."
                )
            elif user_type == 'I' and crn_no:
                # Individual user might have put something by mistake in CRN field, so just get rid of it
                # when entering it into the database
                self.cleaned_data['crn_no'] = '00000000'

            return self.cleaned_data['crn_no']

        raise forms.ValidationError("This CRN is already registered.")

class SDPForm(forms.Form):
    amount=forms.IntegerField(required=True)
    frequency=forms.ChoiceField(required=True,choices=(('W', 'Weekly'), ('F', '15-days'), ('M', 'Monthly'), ('Q', 'Quaterly')))
    