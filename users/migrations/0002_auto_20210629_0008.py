# Generated by Django 2.2.5 on 2021-06-28 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('other', 'Other'), ('female', 'Female')], max_length=10),
        ),
    ]
