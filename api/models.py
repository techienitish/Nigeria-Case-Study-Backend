import requests
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

hostname = settings.BIG_DATA_HOST
port = settings.BIG_DATA_PORT


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
        ],
        default='Analyst',
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='department',
        default=None,
        null=True,
    )

    def __str__(self):
        return self.user.username


def delete_user_on_account_removal(sender, instance, **kwargs):
    user_id = instance.user.id
    user = User.objects.get(pk=user_id)
    user.delete()


post_delete.connect(delete_user_on_account_removal, sender=Account)


class Case(models.Model):
    name = models.CharField(max_length=128, default=None, null=True)
    accounts = models.ManyToManyField(
        Account, blank=True, related_name='accounts'
    )
    targets = ArrayField(
        models.CharField(max_length=128),
        default=list,
    )
    description = models.CharField(max_length=512)
    category = models.CharField(
        max_length=32,
        choices=[
            ('Robbery', 'Robbery'),
            ('Theft', 'Theft'),
            ('Bomb Blast', 'Bomb Blast'),
            ('Other', 'Other'),
        ],
        default='Other'
    )
    status = models.CharField(
        max_length=32,
        choices=[
            ('Open', 'Open'),
            ('Close', 'Close'),
            ('Delayed', 'Delayed')
        ],
        default='Open'
    )
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
        ],
        default='PENDING',
    )
    category = models.CharField(
        max_length=32,
        choices=[
            ('IMSI', 'IMSI'),
            ('IMEI', 'IMEI'),
            ('MSISDN', 'MSISDN'),
            ('Location', 'Location'),
            ('LAC/Cell-ID', 'LAC/Cell-ID'),
        ],
        default='IMSI'
    )
    startTime = models.BigIntegerField(default=-1)
    endTime = models.BigIntegerField(default=-1)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


def create_server_job(sender, instance, **kwargs):
    jobId = instance.id
    query = instance.query
    category = instance.category
    startTime = instance.startTime
    endTime = instance.endTime

    payload = {
        'startTime': startTime,
        'endTime': endTime,
    }

    if category == 'IMSI':
        endpoint = 'http://{}:{}/ontrack-webservice/imsilocations'.format(
            hostname, port)
        payload['imsi'] = query
    elif category == 'IMEI':
        endpoint = 'http://{}:{}/ontrack-webservice/imeilocations'.format(
            hostname, port)
        payload['imei'] = query
    elif category == 'MSISDN':
        endpoint = 'http://{}:{}/ontrack-webservice/msisdnlocations'.format(
            hostname, port)
        payload['msisdn'] = query
    elif category == 'Location':
        queryArr = query.split(',')
        payload['lat'] = queryArr[0]
        payload['lon'] = queryArr[1]
        payload['distance'] = queryArr[2]
        endpoint = 'http://{}:{}/ontrack-webservice/locations'.format(
            hostname, port)
    elif category == 'LAC/Cell-ID':
        queryArr = query.split(',')
        payload['lac'] = queryArr[0].strip()
        payload['cellid'] = queryArr[1].strip()
        payload['distance'] = queryArr[2].strip()
        endpoint = 'http://{}:{}/ontrack-webservice/celllocations'.format(
            hostname, port)

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
    networkcallreference = models.CharField(
        max_length=128, default=None, null=True)
    mscaddress = models.BigIntegerField(default=-1)
    systemtype = models.CharField(max_length=128, default=None, null=True)
    chargedparty = models.CharField(max_length=128, default=None, null=True)
    calledimsi = models.BigIntegerField(default=-1)
    subscribercategory = models.CharField(
        max_length=128, default=None, null=True)
    firstmccmnc = models.CharField(max_length=128, default=None, null=True)
    intermediatemccmnc = models.CharField(
        max_length=128, default=None, null=True)
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
    globalcallreference = models.CharField(
        max_length=128, default=None, null=True)
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
