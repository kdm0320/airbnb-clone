# Generated by Django 2.2.5 on 2021-07-03 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20210703_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'Female'), ('other', 'Other'), ('male', 'Male')], max_length=10),
        ),
    ]
