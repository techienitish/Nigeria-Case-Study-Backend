# Generated by Django 3.0.7 on 2020-07-29 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200729_0809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='eventEndDate',
        ),
        migrations.RemoveField(
            model_name='job',
            name='eventStartDate',
        ),
        migrations.AddField(
            model_name='job',
            name='endTime',
            field=models.BigIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='job',
            name='startTime',
            field=models.BigIntegerField(default=-1),
        ),
    ]