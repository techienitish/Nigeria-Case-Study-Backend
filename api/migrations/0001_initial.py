# Generated by Django 3.0.7 on 2020-07-24 07:57

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
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disabled', models.BooleanField(default=False)),
                ('designation', models.CharField(choices=[('Admin', 'Admin'), ('Supervisor', 'Supervisor'), ('Analyst', 'Analyst')], max_length=32)),
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
                ('permissibleStartDate', models.DateTimeField(blank=True, default=None, null=True)),
                ('permissibleEndDate', models.DateTimeField(blank=True, default=None, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('accounts', models.ManyToManyField(blank=True, related_name='accounts', to='api.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('zone', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(default=None, max_length=128, null=True)),
                ('serverJobId', models.IntegerField(default=-1)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], max_length=32)),
                ('category', models.CharField(choices=[('IMSI', 'IMSI'), ('IMEI', 'IMEI'), ('MSISDN', 'MSISDN'), ('Cell Site', 'Cell Site')], max_length=32)),
                ('eventStartDate', models.DateTimeField(blank=True, default=None, null=True)),
                ('eventEndDate', models.DateTimeField(blank=True, default=None, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Case')),
            ],
        ),
        migrations.CreateModel(
            name='Head',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Account')),
                ('department', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Department')),
            ],
        ),
        migrations.CreateModel(
            name='CallDetailRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geohash', models.CharField(blank=True, default=None, max_length=16, null=True)),
                ('yyyymm', models.BigIntegerField(default=-1)),
                ('timestamp', models.BigIntegerField()),
                ('servedimsi', models.BigIntegerField()),
                ('servedimei', models.BigIntegerField()),
                ('servedmsisdn', models.BigIntegerField()),
                ('callingnumber', models.BigIntegerField()),
                ('callednumber', models.BigIntegerField()),
                ('recordingentity', models.BigIntegerField()),
                ('locationlat', models.FloatField()),
                ('locationlon', models.FloatField()),
                ('seizureordeliverytime', models.BigIntegerField()),
                ('answertime', models.BigIntegerField()),
                ('releasetime', models.BigIntegerField()),
                ('callduration', models.BigIntegerField()),
                ('causeforterm', models.BigIntegerField()),
                ('diagnostics', models.BigIntegerField()),
                ('callreference', models.CharField(max_length=128)),
                ('sequencenumber', models.BigIntegerField()),
                ('networkcallreference', models.CharField(max_length=128)),
                ('mscaddress', models.BigIntegerField()),
                ('systemtype', models.CharField(max_length=128)),
                ('chargedparty', models.CharField(max_length=128)),
                ('calledimsi', models.BigIntegerField()),
                ('subscribercategory', models.CharField(max_length=128)),
                ('firstmccmnc', models.CharField(max_length=128)),
                ('intermediatemccmnc', models.CharField(max_length=128)),
                ('lastmccmnc', models.CharField(max_length=128)),
                ('usertype', models.CharField(max_length=128)),
                ('recordnumber', models.BigIntegerField()),
                ('partyrelcause', models.CharField(max_length=128)),
                ('chargelevel', models.CharField(max_length=128)),
                ('locationnum', models.CharField(max_length=128)),
                ('zonecode', models.CharField(max_length=128)),
                ('accountcode', models.CharField(max_length=128)),
                ('calledimei', models.BigIntegerField()),
                ('drccallid', models.CharField(max_length=128)),
                ('callredirectionflag', models.BigIntegerField()),
                ('globalcallreference', models.CharField(max_length=128)),
                ('calledportedflag', models.BigIntegerField()),
                ('connectednumber', models.CharField(max_length=128)),
                ('smsuserdatatype', models.CharField(max_length=128)),
                ('smstext', models.CharField(max_length=128)),
                ('maxsmsconcated', models.BigIntegerField()),
                ('concatsmsrefnumber', models.BigIntegerField()),
                ('seqnoofcurrentsms', models.BigIntegerField()),
                ('locationestimate', models.BigIntegerField()),
                ('locationupdatetype', models.BigIntegerField()),
                ('imeistatus', models.BigIntegerField()),
                ('job', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='api.Job')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department', to='api.Department'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
