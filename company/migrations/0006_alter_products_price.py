# Generated by Django 4.2.3 on 2023-10-21 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_alter_catalogos_type_catalog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.IntegerField(verbose_name='precio'),
        ),
    ]
