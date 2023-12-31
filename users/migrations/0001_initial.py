# Generated by Django 4.1.1 on 2023-04-02 15:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="StartYoungUKUser",
            fields = [
                ("id", models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=50, null=False, unique=True)),
                ("address", models.TextField(max_length=100)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None, unique=True
                    ),
                ),
                (
                    "crn_no",
                    models.CharField(
                        default="00000000",
                        max_length=8,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=8)
                        ],
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[("I", "Individual"), ("C", "Corporate")], max_length=10
                    ),
                ),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "image",
                    models.ImageField(default="default.jpg", upload_to="profile_pics"),
                ),
                ("is_coordinator", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("is_buddy", models.BooleanField(default=False)),
                ("sdp_amount", models.PositiveIntegerField(default=0)),
                ("sdp_frequency", models.CharField(
                    max_length=10,
                    choices=(
                        ("W", "Weekly"),
                        ("F", "Fortnightly"),
                        ("M", "Monthly"),
                        ("N", "None"),
                    ),
                    default="N")),
            ],
        ),
        migrations.CreateModel(
            name="Buddy",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("description", models.TextField(default="No description yet.")),
                ("date_status_modified", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "pending"),
                            ("approved", "approved"),
                            ("rejected", "rejected"),
                            ("opted_out", "opted out"),
                        ],
                        default="pending",
                        max_length=256,
                    ),
                ),
                ("approver", models.EmailField(max_length=256, null=True)),
                ("letter_received", models.BooleanField(default=False)),
                ("sdp_start",models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterModelOptions(
            name="buddy",
            options={"verbose_name_plural": "Buddies"},
        ),
        migrations.AlterModelOptions(
            name="startyoungukuser",
            options={"verbose_name_plural": "Start Young UK Users"},
        ),

    ]
