from pyexpat import model
from sqlite3 import Timestamp
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator

# Create your models here.

class StartYoungUKUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    address = models.TextField(max_length=100, null=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    # Customer Registration Number (CRN) is UK-equivalent of GST number
    crn_no = models.CharField(default='00000000', max_length=8, validators=[MinLengthValidator(limit_value=8)])
    user_type = models.CharField(max_length=10, choices=[('I', 'Individual'), ('C', 'Corporate')], null=False)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.email}"

class Child(models.Model):
    child_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    age = models.PositiveIntegerField(null=False)
    gender = models.CharField(max_length=10, choices=[('M', 'Female'), ('F', 'Female'), ('O', 'Others')], null=False)
    class_std = models.CharField(max_length=10, null=False)
    school = models.CharField(max_length=50, null=False)
    hobbies = models.CharField(max_length=10,default="0000000000")
    mentor = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_created=True)
    def __str__(self):
        return f"{self.child_id}"   


class Mentor(models.Model):
    mentor_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    hobbies = models.CharField(max_length=10,default="0000000000")
    date = models.DateTimeField(auto_created=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=20, null=False)
    def __str__(self):
        return f"{self.mentor_id}"   

