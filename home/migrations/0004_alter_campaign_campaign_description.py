# Generated by Django 4.1 on 2023-10-07 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_alter_affiliation_affiliation_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="campaign_description",
            field=models.TextField(max_length=1000),
        ),
    ]