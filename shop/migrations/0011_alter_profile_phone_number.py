# Generated by Django 5.1.2 on 2024-10-27 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_profile_options_user_address_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
    ]
