# Generated by Django 4.0.7 on 2023-05-01 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_child_remove_buddy_description_buddy_hobbies_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Child',
        ),
        migrations.RemoveField(
            model_name='buddy',
            name='hobbies',
        ),
        migrations.RemoveField(
            model_name='buddy',
            name='occupation',
        ),
        migrations.AddField(
            model_name='buddy',
            name='description',
            field=models.TextField(default='No description yet.'),
        ),
        migrations.AlterField(
            model_name='buddy',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected'), ('opted_out', 'opted out')], default='pending', max_length=256),
        ),
    ]