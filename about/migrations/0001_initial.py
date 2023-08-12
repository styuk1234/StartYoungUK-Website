# Generated by Django 4.0.7 on 2023-05-01 06:27

import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CharityDetail",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=50, unique=True)),
                ("website", models.CharField(max_length=255)),
                ("address", models.TextField(max_length=100)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None, unique=True
                    ),
                ),
                ("charity_number", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="GalleryItem",
            fields=[
                ("item_id", models.AutoField(primary_key=True, serialize=False)),
                ("item_title", models.CharField(max_length=100)),
                (
                    "item_file",
                    models.FileField(
                        default="default_image.jpg",
                        upload_to="gallery_items",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["mp4", "mov", "docx", "jpg", "png", "jpeg"]
                            )
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                ("member_id", models.AutoField(primary_key=True, serialize=False)),
                ("member_name", models.CharField(max_length=100)),
                ("member_title", models.CharField(max_length=50)),
                (
                    "member_image",
                    models.ImageField(
                        default="default_member.jpg", upload_to="team_member_pics"
                    ),
                ),
            ],
        ),
    ]
