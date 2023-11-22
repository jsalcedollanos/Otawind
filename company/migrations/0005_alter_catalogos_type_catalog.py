# Generated by Django 4.2.3 on 2023-10-18 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_catalogos_type_catalog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogos',
            name='type_catalog',
            field=models.CharField(choices=[('Servicios', 'Servicios'), ('Productos', 'Productos')], max_length=10, verbose_name='Tipo catalogo'),
        ),
    ]