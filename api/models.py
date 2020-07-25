import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=128, default=None, null=True)
    zone = models.CharField(max_length=128, default=None, null=True)
    head = models.CharField(max_length=128, default=None, null=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user'
    )
    disabled = models.BooleanField(default=False)
    designation = models.CharField(
        max_length=32,
        choices=[
            ('Admin', 'Admin'),
            ('Supervisor', 'Supervisor'),
            ('Analyst', 'Analyst'),
        ]
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='department'
    )

    def __str__(self):
        return self.user.username


class Case(models.Model):
    name = models.CharField(max_length=128, default=None, null=True)
    accounts = models.ManyToManyField(
        Account, blank=True, related_name='accounts'
    )
    description = models.CharField(max_length=512)
    category = models.CharField(
        max_length=32,
        choices=[
            ('Robbery', 'Robbery'),
            ('Theft', 'Theft'),
            ('Bomb Blast', 'Bomb Blast'),
        ]
    )
    status = models.CharField(
        max_length=32,
        choices=[
            ('Open', 'Open'),
            ('Close', 'Close'),
            ('Delayed', 'Delayed')
        ]
    )
    permissibleStartDate = models.DateTimeField(default=None, null=True, blank=True)
    permissibleEndDate = models.DateTimeField(default=None, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    query = models.CharField(max_length=128, default=None, null=True)
    serverJobId = models.CharField(max_length=128, default=None, null=True)
    status = models.CharField(
        max_length=32,
        choices=[
            ('PENDING', 'PENDING'),
            ('FINISHED', 'FINISHED')
        ]
    )
    category = models.CharField(
        max_length=32,
        choices=[
            ('IMSI', 'IMSI'),
            ('IMEI', 'IMEI'),
            ('MSISDN', 'MSISDN'),
            ('Cell Site', 'Cell Site'),
        ]
    )
    eventStartDate = models.DateTimeField(default=None, null=True, blank=True)
    eventEndDate = models.DateTimeField(default=None, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


def create_server_job(sender, instance, **kwargs):
    jobId = instance.id
    query = instance.query
    category = instance.category
    eventStartDate = instance.eventStartDate
    eventEndDate = instance.eventEndDate
    payload = {
        'startTime': '1588219377000',   # Should be removed
        'endTime': '1588419377000',
    }
    if category == 'IMSI':
        endpoint = 'http://{}/ontrack-webservice/imsilocations'.format(settings.BIG_DATA_HOST)
        payload['imsi'] = query
    elif category == 'IMEI':
        endpoint = 'http://{}/ontrack-webservice/imeilocations'.format(settings.BIG_DATA_HOST)
        payload['imei'] = query
    elif category == 'MSISDN':
        endpoint = 'http://{}/ontrack-webservice/msisdnlocations'.format(settings.BIG_DATA_HOST)
        payload['msisdn'] = query
    response = requests.get(endpoint, params=payload)
    response = response.json()
    serverJobId = response['requestID']
    Job.objects.filter(pk=jobId).update(serverJobId=serverJobId)

post_save.connect(create_server_job, sender=Job)


class CallDetailRecord(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=-1)
    geohash = models.CharField(
        max_length=16, default=None, null=True, blank=True
    )
    yyyymm = models.BigIntegerField(default=-1, null=True)
    timestamp = models.BigIntegerField(default=-1)
    timebucket = models.CharField(max_length=128, default=None, null=True)
    servedimsi = models.BigIntegerField(default=-1)
    servedimei = models.BigIntegerField(default=-1)
    servedmsisdn = models.BigIntegerField(default=-1)
    callingnumber = models.BigIntegerField(default=-1)
    callednumber = models.BigIntegerField(default=-1)
    recordingentity = models.BigIntegerField(default=-1)
    locationlat = models.FloatField(default=-1)
    locationlon = models.FloatField(default=-1)
    seizureordeliverytime = models.BigIntegerField(default=-1)
    answertime = models.BigIntegerField(default=-1)
    releasetime = models.BigIntegerField(default=-1)
    callduration = models.BigIntegerField(default=-1)
    causeforterm = models.BigIntegerField(default=-1)
    diagnostics = models.BigIntegerField(default=-1)
    callreference = models.CharField(max_length=128, default=None, null=True)
    sequencenumber = models.BigIntegerField(default=-1)
    networkcallreference = models.CharField(max_length=128, default=None, null=True)
    mscaddress = models.BigIntegerField(default=-1)
    systemtype = models.CharField(max_length=128, default=None, null=True)
    chargedparty = models.CharField(max_length=128, default=None, null=True)
    calledimsi = models.BigIntegerField(default=-1)
    subscribercategory = models.CharField(max_length=128, default=None, null=True)
    firstmccmnc = models.CharField(max_length=128, default=None, null=True)
    intermediatemccmnc = models.CharField(max_length=128, default=None, null=True)
    lastmccmnc = models.CharField(max_length=128, default=None, null=True)
    usertype = models.CharField(max_length=128, default=None, null=True)
    recordnumber = models.BigIntegerField(default=-1)
    partyrelcause = models.CharField(max_length=128, default=None, null=True)
    chargelevel = models.CharField(max_length=128, default=None, null=True)
    locationnum = models.CharField(max_length=128, default=None, null=True)
    zonecode = models.CharField(max_length=128, default=None, null=True)
    accountcode = models.CharField(max_length=128, default=None, null=True)
    calledportedflag = models.BigIntegerField(default=-1)
    calledimei = models.BigIntegerField(default=-1)
    drccallid = models.CharField(max_length=128, default=None, null=True)
    callredirectionflag = models.BigIntegerField(default=-1)
    globalcallreference = models.CharField(max_length=128, default=None, null=True)
    callerportedflag = models.BigIntegerField(default=-1)
    connectednumber = models.CharField(max_length=128, default=None, null=True)
    smsuserdatatype = models.CharField(max_length=128, default=None, null=True)
    smstext = models.CharField(max_length=128, default=None, null=True)
    maxsmsconcated = models.BigIntegerField(default=-1)
    concatsmsrefnumber = models.BigIntegerField(default=-1)
    seqnoofcurrentsms = models.BigIntegerField(default=-1)
    locationestimate = models.BigIntegerField(default=-1)
    locationupdatetype = models.BigIntegerField(default=-1)
    imeistatus = models.BigIntegerField(default=-1)
