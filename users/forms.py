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
    user_type = forms.ChoiceField(choices=(('I', 'Individual '), ('C', 'Corporate')),widget=forms.Select(attrs={'class': 'form-select', 'style': 'width: 100%; height:40px'}),required=True)
    email = forms.EmailField(required=True)
    #accept_tou = forms.BooleanField(required=True, label="I agree to the Terms of Use and Privacy.")
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
            initial='GB',  # GB works, not UK
        ),
        required=True,
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
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
        model = StartYoungUKUser
        fields = ['display_name', 'email', 'phone_number', 'address']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['display_name'].widget.attrs.update({'readonly':'readonly'})
        self.fields['display_name'].required=False
        self.fields['email'].widget.attrs.update({'readonly':'readonly'})
        self.fields['email'].required=False
        # self.fields['image'].required=False

    def clean_phone_number(self):
        # Validate unique phone_number
        phone_number = self.cleaned_data["phone_number"]

        try:
            syukuser=StartYoungUKUser.objects.get(phone_number=phone_number)
            if syukuser.email == self.cleaned_data['email']:
                return phone_number
            
        except StartYoungUKUser.DoesNotExist:
            return phone_number
        
        raise forms.ValidationError("This Phone Number is already registered.")


    # image = forms.ImageField()

    email = forms.EmailField(required=True)

    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
            initial='GB',  # GB works, not UK
        ),
        required=True
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=True,
    )
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class SDPForm(forms.Form):
    amount=forms.IntegerField(required=True)
    frequency=forms.ChoiceField(required=True,choices=(('W', 'Weekly'), ('F', 'Fortnightly'), ('M', 'Monthly'), ('Q', 'Quaterly')))