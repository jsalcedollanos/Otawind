# Generated by Django 4.2.3 on 2023-10-21 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_alter_products_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='price',
            field=models.IntegerField(verbose_name='precio'),
        ),
    ]
