from django.db import models
from django.contrib.auth.models import User


class CallDetailRecord(models.Model):
    timestamp = models.IntegerField()
    servedIMSI = models.IntegerField()
    servedIMEI = models.IntegerField()
    servedMSISDN = models.IntegerField()
    callingNumber = models.IntegerField()
    calledNumber = models.IntegerField()
    recordingEntity = models.IntegerField()
    locationLat = models.FloatField()
    locationLon = models.FloatField()
    seizureOrDeliveryTime = models.IntegerField()
    answerTime = models.IntegerField()
    releaseTime = models.IntegerField()
    callDuration = models.IntegerField()
    causeForTerm = models.IntegerField()
    diagnostics = models.IntegerField()
    callReference = models.CharField(max_length=128)
    sequenceNumber = models.IntegerField()
    networkCallReference = models.CharField(max_length=128)
    mscAddress = models.IntegerField()
    systemType = models.CharField(max_length=128)
    chargedParty = models.CharField(max_length=128)
    calledIMSI = models.IntegerField()
    subscriberCategory = models.CharField(max_length=128)
    firstMccMnc = models.CharField(max_length=128)
    intermediateMccMnc = models.CharField(max_length=128)
    lastMccMnc = models.CharField(max_length=128)
    userType = models.CharField(max_length=128)
    recordNumber = models.IntegerField()
    partyRelCause = models.CharField(max_length=128)
    chargeLevel = models.CharField(max_length=128)
    locationNum = models.CharField(max_length=128)
    zoneCode = models.CharField(max_length=128)
    accountCode = models.CharField(max_length=128)
    calledPortedFlag = models.CharField(max_length=128)
    calledIMEI = models.IntegerField()
    drcCallId = models.CharField(max_length=128)
    callRedirectionFlag = models.IntegerField()
    globalCallReference = models.CharField(max_length=128)
    calledPortedFlag = models.IntegerField()
    connectedNumber = models.CharField(max_length=128)
    smsUserDataType = models.CharField(max_length=128)
    smsText = models.CharField(max_length=128)
    maxSMSConcated = models.IntegerField()
    concatSMSRefNumber = models.IntegerField()
    seqNoOfCurrentSMS = models.IntegerField()
    locationEstimate = models.IntegerField()
    locationUpdateType = models.IntegerField()
    imeiStatus = models.IntegerField()


class Case(models.Model):
    name = models.CharField(max_length=128)
    supervisors = models.ManyToManyField(
        User, blank=True, related_name='supervisors')
    analysts = models.ManyToManyField(
        User, blank=True, related_name='analysts')
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
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    serverJobId = models.IntegerField()
    results = models.ManyToManyField(CallDetailRecord, blank=True)
    status = models.CharField(
        max_length=32,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed')
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
