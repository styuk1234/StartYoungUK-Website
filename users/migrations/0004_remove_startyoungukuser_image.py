# Generated by Django 4.2.4 on 2023-08-13 10:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_startyoungukuser_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="startyoungukuser",
            name="image",
        ),
    ]
