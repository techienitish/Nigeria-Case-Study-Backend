# Generated by Django 3.0.7 on 2020-08-11 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20200811_0828'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Department'),
        ),
        migrations.AddField(
            model_name='case',
            name='endDate',
            field=models.BigIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='case',
            name='startDate',
            field=models.BigIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='case',
            name='teamLead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Account'),
        ),
    ]
