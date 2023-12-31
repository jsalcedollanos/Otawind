# Generated by Django 4.2.3 on 2023-10-09 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='bio',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='city',
            field=models.CharField(default=1, max_length=50, verbose_name='Ciudad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='email',
            field=models.EmailField(default=2, max_length=254, verbose_name='Correo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='facebook',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='instagram',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='whatsapp',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
