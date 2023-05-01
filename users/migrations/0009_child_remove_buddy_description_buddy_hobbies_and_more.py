# Generated by Django 4.0.7 on 2023-04-29 19:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_delete_child_remove_buddy_hobbies_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('date', models.DateTimeField(auto_created=True)),
                ('child_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], max_length=10)),
                ('class_std', models.CharField(max_length=10)),
                ('school', models.CharField(max_length=50)),
                ('hobbies', models.CharField(default='0000000000', max_length=10)),
                ('mentor', models.PositiveIntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Children',
            },
        ),
        migrations.RemoveField(
            model_name='buddy',
            name='description',
        ),
        migrations.AddField(
            model_name='buddy',
            name='hobbies',
            field=models.CharField(default='0000000000', max_length=10),
        ),
        migrations.AddField(
            model_name='buddy',
            name='occupation',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buddy',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected'), ('opted out', 'opted out')], default='pending', max_length=256),
        ),
    ]