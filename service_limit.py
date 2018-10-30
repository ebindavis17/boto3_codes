#Python script checks for the services that are hitting 80 % limit. Normally Trusted Advisor helps to find the service limits.
#This script uses Trusted advisor boto3 function to fetch all the services that are hitting 80 % and outputs to a CSV file.

#Note: Trusted advisor support only few servi
import boto3
import csv
from botocore.exceptions import ClientError
import logging
import re
logger = logging.getLogger()
role_name='aab-administrator'
region=[]
servicename=[]
resource=[]
limit_amount=[]
current_usage=[]
account=[]
status=[]


def service_limit_check(account_details):
    checkid=[]
    for credentials_list in assume_role_accnt(account_id_list):
      client=boto3.client('support','us-east-1',aws_access_key_id=credentials_list['aws_access_key_id'], aws_secret_access_key=credentials_list['aws_secret_access_key'], aws_session_token=credentials_list['aws_session_token'])

      trustedadvisor_checks = client.describe_trusted_advisor_checks(
       language="en"
      )


      for service in trustedadvisor_checks['checks']:

       if service['category'] == 'service_limits':
        if service['id'] not in checkid:

         checkid.append(service['id'])

      for allcheckids in checkid:

       trustedadvisor_result = client.describe_trusted_advisor_check_result(
         checkId=allcheckids,
         language='en'
       )


       for checkresult in trustedadvisor_result['result']['flaggedResources']:

         if checkresult['status'] == 'warning' or  checkresult['status'] == 'error':
          region.append(checkresult['metadata'][0])
          servicename.append(checkresult['metadata'][1])
          resource.append(checkresult['metadata'][2])
          limit_amount.append(checkresult['metadata'][3])
          current_usage.append(checkresult['metadata'][4])
          account.append(account_details[credentials_list['account_id']])
          status.append('WARNING')

    limit_details=zip(region,servicename,resource,limit_amount, current_usage,account,status)
    header = ['Region', 'Service','Resource','Limit Amount','Current Usage','Account','Status']
    csvfile = "/tmp/testingS3.csv"
    with open(csvfile, "w") as testing:
          writer = csv.writer(testing, lineterminator='\n')
          writer.writerow(header)
          writer.writerows(limit_details)

def s3(account_details):
    for credentials_list in assume_role_accnt(account_id_list):
      client_buckets=boto3.client('s3',aws_access_key_id=credentials_list['aws_access_key_id'], aws_secret_access_key=credentials_list['aws_secret_access_key'], aws_session_token=credentials_list['aws_session_token'])

      buckets=[]

      buckets_list= client_buckets.list_buckets()
      for i in buckets_list['Buckets']:
        buckets.append(i['Name'])
      if len(buckets) > 80 :

        region.append("eu-west-1")
        servicename.append("S3")
        resource.append("Buckets")
        limit_amount.append("-")
        current_usage.append(len(buckets))
        account.append(account_details[credentials_list['account_id']])
        status.append("WARNING")


    limit_details=zip(region,servicename,resource,limit_amount,current_usage,account,status)
    header = ['Region','Service','Resource','Limit Amount','Current Usage','Account','Status']
    csvfile = "/path/to/savetheresult.csv"
    with open(csvfile, "w") as testing:
          writer = csv.writer(testing, lineterminator='\n')
          writer.writerow(header)
          writer.writerows(limit_details)

def ec2(account_details):
    for credentials_list in assume_role_accnt(account_id_list):
      client_buckets=boto3.client('ec2',aws_access_key_id=credentials_list['aws_access_key_id'], aws_secret_access_key=credentials_list['aws_secret_access_key'], aws_session_token=credentials_list['aws_session_token'])


service_limit_check(account_details)
s3(account_details)
