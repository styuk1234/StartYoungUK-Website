# Generated by Django 4.1.5 on 2023-03-14 16:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sponsor", "0004_alter_donation_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="is_successful",
            field=models.BooleanField(default=False),
        ),
    ]