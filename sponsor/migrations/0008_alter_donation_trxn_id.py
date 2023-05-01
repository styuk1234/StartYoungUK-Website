# Generated by Django 4.0.7 on 2023-05-01 06:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0007_alter_donation_trxn_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='trxn_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
