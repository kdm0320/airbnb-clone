# Generated by Django 2.2.5 on 2021-08-01 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20210731_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_secret',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
