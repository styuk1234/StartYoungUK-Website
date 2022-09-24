from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import DecimalValidator, MinLengthValidator

# Create your models here.

class StartYoungUKUsers(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, null=False)
    email_id = models.EmailField(max_length=50, null=False, unique=True)
    address = models.EmailField(max_length=100, null=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    # Customer Registration Number (CRN) is UK-equivalent of GST number
    crn_no = models.IntegerField(null=True, validators=[DecimalValidator(max_digits=8, decimal_places=8)], unique=True)
    user_type = models.CharField(max_length=10, choices=[('I', 'Individual'), ('C', 'Corporate')], null=False, unique=True)
    is_verified = models.BooleanField(default=False)