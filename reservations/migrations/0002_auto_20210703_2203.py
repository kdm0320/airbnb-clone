# Generated by Django 2.2.5 on 2021-07-03 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='check_in',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='check_out',
            field=models.DateField(auto_now=True),
        ),
    ]
