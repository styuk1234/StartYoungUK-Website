from pyexpat import model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Donations(models.Model):
    trxn_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50, null=False)
    email_id=models.EmailField(max_length=50, null=False)
    mobile_no=PhoneNumberField(null=False,blank=False)
    amount=models.PositiveIntegerField(null=False)
    user_id=models.IntegerField(null=False, default=0)
