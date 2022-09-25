from xml.dom import ValidationErr
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from users.models import StartYoungUKUser


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
    address = forms.CharField(
                                widget=forms.Textarea(),
                                required=True,
                            )
    crn_no = forms.CharField(label="Company Registration Number (CRN)", required=False, help_text="If you're signing up as a corporate, please enter your CRN")
    
    class Meta:
        model = User
        fields = ['display_name', 'user_type', 'email', 'phone_number', 'address', 'crn_no', 'username', 'password1','password2']

    def clean_email(self):
        #Validate unique email
        email = self.cleaned_data["email"]

        try:
            match_email = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
            
        raise forms.ValidationError('This email is already registered.')
    
    
    def clean_phone_number(self):
        from phonenumber_field.phonenumber import PhoneNumber

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
            StartYoungUKUser.objects.get(crn_no=crn_no)

        except StartYoungUKUser.DoesNotExist:
            if user_type == 'C' and not crn_no:
            # If user is corporate type but has not entered CRN, prompt validation error
                raise ValidationError(
                    "If you're a corporate user, please enter your CRN for validation."
                )
            elif user_type == 'I' and crn_no:
            # Individual user might have put something by mistake in CRN field, so just get rid of it
            # when entering it into the database
                self.cleaned_data['crn_no'] = '00000000'

            return crn_no
            
        raise forms.ValidationError("This CRN is already registered.")