# Generated by Django 4.0.7 on 2023-05-03 09:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_delete_child_remove_buddy_hobbies_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="startyoungukuser",
            name="display_name",
        ),
    ]