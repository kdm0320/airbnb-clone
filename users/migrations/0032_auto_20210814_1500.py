# Generated by Django 2.2.5 on 2021-08-14 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_auto_20210814_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.CharField(blank=True, choices=[('usd', 'USD'), ('krw', 'KRW')], max_length=3),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_secret',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
