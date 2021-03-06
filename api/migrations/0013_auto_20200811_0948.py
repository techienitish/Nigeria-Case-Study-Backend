# Generated by Django 3.0.7 on 2020-08-11 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200811_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=128, null=True)),
                ('description', models.CharField(default=None, max_length=512, null=True)),
                ('lat1', models.FloatField(default=-1)),
                ('lng1', models.FloatField(default=-1)),
                ('lat2', models.FloatField(default=-1)),
                ('lng2', models.FloatField(default=-1)),
                ('area', models.FloatField(default=-1)),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='zone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Zone'),
        ),
    ]
