# Generated by Django 2.2.5 on 2021-07-02 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='cLocation',
            new_name='Location',
        ),
    ]
