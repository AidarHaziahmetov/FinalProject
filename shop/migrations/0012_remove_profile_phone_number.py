# Generated by Django 5.1.2 on 2024-10-27 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_profile_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
    ]
