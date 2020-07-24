from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=128)
    zone = models.CharField(max_length=128)

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


class Head(models.Model):
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username + '-' + self.department.name


class Case(models.Model):
    name = models.CharField(max_length=128)
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
    serverJobId = models.IntegerField(default=-1)
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


class CallDetailRecord(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=-1)
    geohash = models.CharField(
        max_length=16, default=None, null=True, blank=True
    )
    yyyymm = models.BigIntegerField(default=-1)
    timestamp = models.BigIntegerField()
    servedimsi = models.BigIntegerField()
    servedimei = models.BigIntegerField()
    servedmsisdn = models.BigIntegerField()
    callingnumber = models.BigIntegerField()
    callednumber = models.BigIntegerField()
    recordingentity = models.BigIntegerField()
    locationlat = models.FloatField()
    locationlon = models.FloatField()
    seizureordeliverytime = models.BigIntegerField()
    answertime = models.BigIntegerField()
    releasetime = models.BigIntegerField()
    callduration = models.BigIntegerField()
    causeforterm = models.BigIntegerField()
    diagnostics = models.BigIntegerField()
    callreference = models.CharField(max_length=128)
    sequencenumber = models.BigIntegerField()
    networkcallreference = models.CharField(max_length=128)
    mscaddress = models.BigIntegerField()
    systemtype = models.CharField(max_length=128)
    chargedparty = models.CharField(max_length=128)
    calledimsi = models.BigIntegerField()
    subscribercategory = models.CharField(max_length=128)
    firstmccmnc = models.CharField(max_length=128)
    intermediatemccmnc = models.CharField(max_length=128)
    lastmccmnc = models.CharField(max_length=128)
    usertype = models.CharField(max_length=128)
    recordnumber = models.BigIntegerField()
    partyrelcause = models.CharField(max_length=128)
    chargelevel = models.CharField(max_length=128)
    locationnum = models.CharField(max_length=128)
    zonecode = models.CharField(max_length=128)
    accountcode = models.CharField(max_length=128)
    calledportedflag = models.CharField(max_length=128)
    calledimei = models.BigIntegerField()
    drccallid = models.CharField(max_length=128)
    callredirectionflag = models.BigIntegerField()
    globalcallreference = models.CharField(max_length=128)
    calledportedflag = models.BigIntegerField()
    connectednumber = models.CharField(max_length=128)
    smsuserdatatype = models.CharField(max_length=128)
    smstext = models.CharField(max_length=128)
    maxsmsconcated = models.BigIntegerField()
    concatsmsrefnumber = models.BigIntegerField()
    seqnoofcurrentsms = models.BigIntegerField()
    locationestimate = models.BigIntegerField()
    locationupdatetype = models.BigIntegerField()
    imeistatus = models.BigIntegerField()
