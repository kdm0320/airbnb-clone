# Generated by Django 2.2.5 on 2021-07-30 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_auto_20210714_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.CharField(blank=True, choices=[('usd', 'USD'), ('krw', 'KRW')], default='krw', max_length=3),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('english', 'English'), ('korean', 'Korean')], default='korean', max_length=6),
        ),
    ]
