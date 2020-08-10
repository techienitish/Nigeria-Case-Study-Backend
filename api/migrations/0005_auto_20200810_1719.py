# Generated by Django 3.0.7 on 2020-08-10 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_job_handsethistorystatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handsethistory',
            name='history_type',
            field=models.CharField(choices=[('imsi', 'imsi'), ('imei', 'imei'), ('msisdn', 'msisdn')], db_column='type', default='imsi', max_length=32),
        ),
    ]
