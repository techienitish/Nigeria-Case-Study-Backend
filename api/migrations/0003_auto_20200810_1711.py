# Generated by Django 3.0.7 on 2020-08-10 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_job_handsethistoryjobid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handsethistory',
            name='history_type',
            field=models.CharField(choices=[('imsi', 'imsi'), ('imei', 'imei'), ('msisdn', 'msisdn')], default='imsi', max_length=32),
        ),
    ]