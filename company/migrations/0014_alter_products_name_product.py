# Generated by Django 4.2.3 on 2023-11-17 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_products_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='name_product',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
    ]
