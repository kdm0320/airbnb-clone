# Generated by Django 2.2.5 on 2021-07-30 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0009_auto_20210704_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='guests',
            field=models.IntegerField(blank=True, help_text='How many people will be staying?', null=True),
        ),
    ]
