# Generated by Django 5.1.2 on 2024-10-22 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_brand_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
