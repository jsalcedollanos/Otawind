# Generated by Django 4.2.3 on 2023-11-17 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_products_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='brand',
            field=models.CharField(default=1, max_length=30, verbose_name='Marca'),
            preserve_default=False,
        ),
    ]
