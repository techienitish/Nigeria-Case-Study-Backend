# Generated by Django 3.0.7 on 2020-08-11 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200811_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='endDate',
            field=models.BigIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='account',
            name='startDate',
            field=models.BigIntegerField(default=-1),
        ),
    ]
