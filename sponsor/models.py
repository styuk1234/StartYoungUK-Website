from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class Donation(models.Model):
    # trxn_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, primary_key=True)
    trxn_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    campaign_id = models.IntegerField(null=False, default=0)
    user_id = models.IntegerField(null=False, default=0)
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False)
    mobile_number = PhoneNumberField(null=False,blank=False)
    amount = models.PositiveIntegerField(null=False)
    is_anonymous = models.BooleanField(null=False, default=False)
    is_successful = models.BooleanField(null=False, default=False)
    date_donation = models.DateTimeField(auto_now_add=True)