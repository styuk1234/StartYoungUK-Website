from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator

# Create your models here.


class StartYoungUKUser(models.Model):
    class Meta:
        verbose_name_plural = "Start Young UK Users"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, null=False, unique=True)
    address = models.TextField(max_length=100, null=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, verbose_name="Phone Number")
    # Customer Registration Number (CRN) is UK-equivalent of GST number
    crn_no = models.CharField(
        default="00000000", max_length=8, validators=[MinLengthValidator(limit_value=8)],
        verbose_name="CRN Number"
    )
    user_type = models.CharField(
        max_length=10, choices=[("I", "Individual"), ("C", "Corporate")], null=False
    )
    is_verified = models.BooleanField(default=False)
    is_coordinator = models.BooleanField(default=False)
    is_buddy = models.BooleanField(default=False)
    sdp_amount = models.PositiveIntegerField(default=0, verbose_name="RDP Amount")
    sdp_frequency = models.CharField(
        max_length=10,
        choices=(
            ("W", "Weekly"),
            ("F", "Fortnightly"),
            ("M", "Monthly"),
            ("N", "None"),
        ),
        default="N",
        verbose_name="RDP Frequency"
    )

    def __str__(self):
        return f"{self.email}"


class Buddy(models.Model):
    class Meta:
        verbose_name_plural = "Buddies"

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(null=False, default="No description yet.")
    date_status_modified = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=256,
        choices=[
            ("pending", "pending"),
            ("approved", "approved"),
            ("rejected", "rejected"),
            ("opted_out", "opted out"),
        ],
        default="pending",
    )
    approver = models.EmailField(max_length=256, null=True)
    letter_received = models.BooleanField(default=False)
    sdp_start = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"
