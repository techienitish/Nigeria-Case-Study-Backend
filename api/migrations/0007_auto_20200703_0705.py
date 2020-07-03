# Generated by Django 3.0.7 on 2020-07-03 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200701_1128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='results',
        ),
        migrations.AddField(
            model_name='calldetailrecord',
            name='job',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='api.Job'),
        ),
        migrations.AlterField(
            model_name='job',
            name='serverJobId',
            field=models.IntegerField(default=-1),
        ),
    ]
