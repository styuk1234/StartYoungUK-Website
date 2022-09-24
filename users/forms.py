from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class UserRegisterForm(UserCreationForm):
    
    display_name = forms.CharField(required=True)
    user_type = forms.ChoiceField(choices=(('I', 'Individual'), ('C', 'Corporate')), required=True)
    email = forms.EmailField(required=True)
    phone_number = PhoneNumberField(
                                widget=PhoneNumberPrefixWidget(
                                    initial='GB', #GB works, not UK
                                ),
                                required=True,
                                )
    address = forms.CharField(required=True)
    Company_Registration_Number = forms.CharField(required=False, help_text="If you're signing up as a corporate, please enter your CRN")
    
    class Meta:
        model = User
        fields = ['display_name', 'user_type', 'email', 'phone_number', 'address', 'Company_Registration_Number', 'username', 'password1','password2']