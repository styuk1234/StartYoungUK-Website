# Generated by Django 4.0.7 on 2023-05-03 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='member_description',
        ),
    ]
