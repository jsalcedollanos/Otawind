# Generated by Django 4.2.3 on 2023-11-22 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0016_alter_catalogos_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogos',
            name='description',
            field=models.TextField(max_length=1000, null=True, verbose_name='descripcion'),
        ),
    ]
