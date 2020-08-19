import uuid
import requests
import paramiko
import pyarrow.parquet as pq
import numpy as np
from sqlalchemy import create_engine
from django.conf import settings
from django_cron import CronJobBase, Schedule
from .models import Job

paramiko.util.log_to_file('./paramiko.log')

hostname = settings.BIG_DATA_HOST
port = settings.BIG_DATA_PORT

statusEndpoint = 'http://{}:{}/ontrack-webservice/status'.format(
    hostname,
    port
)

username = settings.BIG_DATA_USERNAME
keyFilePath = settings.BIG_DATA_HOST_PRIVATE_KEY_FILE_PATH
password = settings.BIG_DATA_HOST_PASSWORD

def ingestParquetFile(localJobId):
    df = pq.read_table(source='temp.parquet').to_pandas()
    df['job_id'] = localJobId
    df.columns = map(str.lower, df.columns)
    str_df = df.select_dtypes([np.object])
    str_df = str_df.stack().str.decode('utf-8').unstack()

    for col in str_df:
        df[col] = str_df[col]

    engine = create_engine(
        'postgresql://ghost:password@localhost:5432/devdb'
    )
    df.to_sql('api_calldetailrecord', engine, if_exists='append', index=False)


def ingestHandsetHistoryParquetFile(localJobId):
    df = pq.read_table(source='temp.parquet').to_pandas()
    df = df[df['type'].notnull()]
    df['job_id'] = localJobId
    df.columns = map(str.lower, df.columns)
    str_df = df.select_dtypes([np.object])
    str_df = str_df.stack().str.decode('utf-8').unstack()

    for col in str_df:
        df[col] = str_df[col]

    engine = create_engine(
        'postgresql://ghost:password@localhost:5432/devdb'
    )
    df.to_sql('api_handsethistory', engine, if_exists='append', index=False)


class FetchRecordsFromBigData(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = str(uuid.uuid4())

    def do(self):
        pendingJobs = Job.objects.filter(status='PENDING')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password = password)
        sftp = ssh.open_sftp()
        localFilePath = 'temp.parquet'

        for job in pendingJobs:
            localJobId = job.id
            payload = {'requestID': job.serverJobId}
            try:
                response = requests.get(statusEndpoint, params=payload)
                response = response.json()
                if response['status'] == 'FINISHED':
                    remoteFilePath = response['outputFile']
                    #remoteFilePath = '/home/centos/autodata/Output/f6069e87-a0e0-4842-9081-b49e451a7e5f/response.parquet'
                    sftp.get(remoteFilePath, localFilePath)
                    ingestParquetFile(localJobId)
                    Job.objects.filter(pk=localJobId).update(status='FINISHED')

            except Exception as ex:
                print('Error for job id: {}'.format(job.serverJobId))
                print(ex)

        # Handset History
        pendingJobs = Job.objects.filter(handsetHistoryStatus='PENDING')
        for job in pendingJobs:
            localJobId = job.id
            payload = {'requestID': job.handsetHistoryJobId}
            try:
                response = requests.get(statusEndpoint, params=payload)
                response = response.json()
                if response['status'] == 'FINISHED':
                    remoteFilePath = response['outputFile']
                    #remoteFilePath = '/home/centos/autodata/Output/f6069e87-a0e0-4842-9081-b49e451a7e5f/response.parquet'
                    sftp.get(remoteFilePath, localFilePath)
                    ingestHandsetHistoryParquetFile(localJobId)
                    Job.objects.filter(pk=localJobId).update(
                        handsetHistoryStatus='FINISHED')

            except Exception as ex:
                print('Error for job id: {}'.format(job.serverJobId))
                print(ex)

        sftp.close()
        ssh.close()
