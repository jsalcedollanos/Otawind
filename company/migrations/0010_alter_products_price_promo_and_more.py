# Generated by Django 4.2.3 on 2023-10-27 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_products_price_promo_products_valoration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price_promo',
            field=models.IntegerField(default='0', verbose_name='promocion'),
        ),
        migrations.AlterField(
            model_name='services',
            name='price_promo',
            field=models.IntegerField(default='0', verbose_name='promocion'),
        ),
    ]
