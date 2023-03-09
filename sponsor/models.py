from wsgiref.validate import validator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Donation(models.Model):
    trxn_id = models.AutoField(primary_key=True)
    campaign_id = models.IntegerField(null=False, default=0)
    user_id = models.IntegerField(null=False, default=0)
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False)
    mobile_number = PhoneNumberField(null=False,blank=False)
    amount = models.PositiveIntegerField(null=False)
    is_anonymous = models.BooleanField(null=False, default=False)