import uuid
import requests
from django.conf import settings
from django_cron import CronJobBase, Schedule
from .models import Job

statusEndpoint = 'http://{}/ontrack-webservice/status'.format(
    settings.BIG_DATA_HOST)


class FetchRecordsFromBigData(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = str(uuid.uuid4())

    def do(self):
        pendingJobs = Job.objects.filter(status='PENDING')
        for job in pendingJobs:
            payload = {'requestID': job.serverJobId}
            try:
                response = requests.get(statusEndpoint, params=payload)
                response = response.json()
                if response['status'] == 'FINISHED':
                    cdrParquetFilePath = response['outputFile']
                    print(cdrParquetFilePath)
            except Exception as ex:
                print('Invalid server job id: {}'.format(job.serverJobId))
