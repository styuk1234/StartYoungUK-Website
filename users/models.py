from pyexpat import model
from sqlite3 import Timestamp
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator

# Create your models here.

class StartYoungUKUser(models.Model):

    class Meta:
        verbose_name_plural = "StartYoung UK Users"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, null=False, unique=True)
    address = models.TextField(max_length=100, null=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    # Customer Registration Number (CRN) is UK-equivalent of GST number
    crn_no = models.CharField(default='00000000', max_length=8, validators=[MinLengthValidator(limit_value=8)])
    user_type = models.CharField(max_length=10, choices=[('I', 'Individual'), ('C', 'Corporate')], null=False)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_coordinator = models.BooleanField(default=False)
    is_buddy = models.BooleanField(default=False)
    sdp_amount = models.PositiveIntegerField(default=0)
    sdp_frequency = models.CharField(max_length=10, choices=(('W', 'Weekly'), ('F', 'Fortnightly'), ('M', 'Monthly'), ('N', 'None')), default='N')

    def __str__(self):
        return f"{self.email}"

# class Child(models.Model):

#     class Meta:
#         verbose_name_plural = "Children"

#     child_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50, null=False)
#     age = models.PositiveIntegerField(null=False)
#     gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], null=False)
#     class_std = models.CharField(max_length=10, null=False)
#     school = models.CharField(max_length=50, null=False)
#     hobbies = models.CharField(max_length=10,default="0000000000")
#     mentor = models.PositiveIntegerField(null=True)
#     date = models.DateTimeField(auto_created=True)
    
#     def __str__(self):
#         return f"{self.child_id}"   

# TODO do we want to make this a child model of startyoung uk user?
class Buddy(models.Model):

    class Meta:
        verbose_name_plural = "Buddies"

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=50, null=False)
    # hobbies = models.CharField(max_length=10,default="0000000000")
    description = models.TextField(null=False, default = "No description yet.")
    date_status_modified = models.DateTimeField(auto_now_add=True)
    # occupation = models.CharField(max_length=20, null=False)
    status = models.CharField(max_length=256,choices=[('pending','pending'),('approved','approved'),('rejected','rejected'),('opted_out','opted out')],default='pending')
    approver = models.EmailField(max_length=256, null=True)
    letter_received = models.BooleanField(default=False)
    sdp_start = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id}"
