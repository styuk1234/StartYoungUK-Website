# Generated by Django 4.1.5 on 2023-03-24 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_campaign_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='slug',
            field=models.SlugField(default='new', unique=True),
            preserve_default=False,
        ),
    ]