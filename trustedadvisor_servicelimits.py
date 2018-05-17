import boto3
import csv
from botocore.exceptions import ClientError
import logging
import re
logger = logging.getLogger()
role_name='*******'
region=[]
service=[]
resource=[]
limit_amount=[]
current_usage=[]
account=[]
status=[]


account_id_list=['***********']

account_details={'***:***']


def get_assumed_credentials(account_id, role_name):

    sts_client = boto3.client('sts')

    try:
        assume_role_object = sts_client.assume_role(
            RoleArn='arn:aws:iam::%s:role/%s' % (account_id, role_name),
            RoleSessionName='session'
        )

    except ClientError as e:
        logger.error('AssumeRole for %s in %s failed with: %s' % (role_name, account_id,
                                                                  e.response['Error']['Message']))

    else:
        logger.debug('AssumeRole succeeded for %s in %s' % (role_name, account_id))
        # From the response that contains the assumed role, get the temporary
        # credentials that can be used to make subsequent API calls.
        return assume_role_object['Credentials']

def assume_role_accnt(account_id_list):
    for id in account_id_list:
        credentials=get_assumed_credentials(id, role_name)
        assumed_credentials_per_profile = {
        'aws_access_key_id': credentials['AccessKeyId'],
        'aws_secret_access_key': credentials['SecretAccessKey'],
        'aws_session_token': credentials['SessionToken'],
        'account_id': id
        }
        yield assumed_credentials_per_profile


def service_limit_check(account_details):
    checkid=[]
    for credentials_list in assume_role_accnt(account_id_list):
      client=boto3.client('support','us-east-1',aws_access_key_id=credentials_list['aws_access_key_id'], aws_secret_access_key=credentials_list['aws_secret_access_key'], aws_session_token=credentials_list['aws_session_token'])

      response = client.describe_trusted_advisor_checks(
       language="en"
      )


      for i in response['checks']:

       if i['category'] == 'service_limits':
        if i['id'] not in checkid:

         checkid.append(i['id'])


      for id1 in checkid:

       response1 = client.describe_trusted_advisor_check_result(
         checkId=id1,
         language='en'
       )


       for i in response1['result']['flaggedResources']:

         if i['status'] == 'warning' or  i['status'] == 'error':
          region.append(i['metadata'][0])
          service.append(i['metadata'][1])
          resource.append(i['metadata'][2])
          limit_amount.append(i['metadata'][3])
          current_usage.append(i['metadata'][4])
          account.append(account_details[credentials_list['account_id']])
          status.append('WARNING')


    limit_details=zip(region,service,resource,limit_amount, current_usage,account,status)
    header = ['Region', 'Service','Resource','Limit Amount','Current Usage','Account','Status']
    csvfile = "/home/ebin.davis/test/sample/testing.csv"
    with open(csvfile, "w") as testing:
          writer = csv.writer(testing, lineterminator='\n')
          writer.writerow(header)
          writer.writerows(limit_details)

service_limit_check(account_details)
