# Generated by Django 4.2.3 on 2023-10-27 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_alter_services_options_alter_services_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='price_promo',
            field=models.IntegerField(default=30000, verbose_name='promocion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='valoration',
            field=models.DecimalField(decimal_places=1, default='3.5', max_digits=2),
        ),
        migrations.AddField(
            model_name='services',
            name='price_promo',
            field=models.IntegerField(default=30000, verbose_name='promocion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='services',
            name='valoration',
            field=models.DecimalField(decimal_places=1, default='3.5', max_digits=2),
        ),
    ]
