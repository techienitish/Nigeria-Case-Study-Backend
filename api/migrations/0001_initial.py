# Generated by Django 3.0.7 on 2020-06-24 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CallDetailRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.IntegerField()),
                ('servedIMSI', models.IntegerField()),
                ('servedIMEI', models.IntegerField()),
                ('servedMSISDN', models.IntegerField()),
                ('callingNumber', models.IntegerField()),
                ('calledNumber', models.IntegerField()),
                ('recordingEntity', models.IntegerField()),
                ('locationLat', models.FloatField()),
                ('locationLon', models.FloatField()),
                ('seizureOrDeliveryTime', models.IntegerField()),
                ('answerTime', models.IntegerField()),
                ('releaseTime', models.IntegerField()),
                ('callDuration', models.IntegerField()),
                ('causeForTerm', models.IntegerField()),
                ('diagnostics', models.IntegerField()),
                ('callReference', models.CharField(max_length=128)),
                ('sequenceNumber', models.IntegerField()),
                ('networkCallReference', models.CharField(max_length=128)),
                ('mscAddress', models.IntegerField()),
                ('systemType', models.CharField(max_length=128)),
                ('chargedParty', models.CharField(max_length=128)),
                ('calledIMSI', models.IntegerField()),
                ('subscriberCategory', models.CharField(max_length=128)),
                ('firstMccMnc', models.CharField(max_length=128)),
                ('intermediateMccMnc', models.CharField(max_length=128)),
                ('lastMccMnc', models.CharField(max_length=128)),
                ('userType', models.CharField(max_length=128)),
                ('recordNumber', models.IntegerField()),
                ('partyRelCause', models.CharField(max_length=128)),
                ('chargeLevel', models.CharField(max_length=128)),
                ('locationNum', models.CharField(max_length=128)),
                ('zoneCode', models.CharField(max_length=128)),
                ('accountCode', models.CharField(max_length=128)),
                ('calledIMEI', models.IntegerField()),
                ('drcCallId', models.CharField(max_length=128)),
                ('callRedirectionFlag', models.IntegerField()),
                ('globalCallReference', models.CharField(max_length=128)),
                ('calledPortedFlag', models.IntegerField()),
                ('connectedNumber', models.CharField(max_length=128)),
                ('smsUserDataType', models.CharField(max_length=128)),
                ('smsText', models.CharField(max_length=128)),
                ('maxSMSConcated', models.IntegerField()),
                ('concatSMSRefNumber', models.IntegerField()),
                ('seqNoOfCurrentSMS', models.IntegerField()),
                ('locationEstimate', models.IntegerField()),
                ('locationUpdateType', models.IntegerField()),
                ('imeiStatus', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=512)),
                ('category', models.CharField(choices=[('Robbery', 'Robbery'), ('Theft', 'Theft'), ('Bomb Blast', 'Bomb Blast')], max_length=32)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Close', 'Close'), ('Delayed', 'Delayed')], max_length=32)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('analyst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serverJobId', models.IntegerField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], max_length=32)),
                ('category', models.CharField(choices=[('IMSI', 'IMSI'), ('IMEI', 'IMEI'), ('MSISDN', 'MSISDN'), ('Cell Site', 'Cell Site')], max_length=32)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Case')),
                ('results', models.ManyToManyField(blank=True, to='api.CallDetailRecord')),
            ],
        ),
    ]
