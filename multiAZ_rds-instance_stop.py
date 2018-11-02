#This  ptyhon boto3 script ensures that RDS databases are stopped on a daily basis (can be done by running this script - eg: using CW events)
#on your AWS accounts ;
#This helps in unwanted cost utilized on the unused DB instances running on your account.

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html

#Note : this script was written when there was no permission given for Multi-AZ DB instance to Stop the instances.

import boto3

client = boto3.client('rds')

dbmultiAZ = []
finalbd = []
new = []

def lambda_handler(event,context):
    response1=client.describe_db_instances()
    
    for i in response1['DBInstances']:
        if i['DBInstanceStatus'] == 'available':
            
            if i['MultiAZ'] == True:
                response2 = client.modify_db_instance(
                    DBInstanceIdentifier=i['DBInstanceIdentifier'],
                    ApplyImmediately=True,
                    MultiAZ=False
                    )
            
        
            else:
                if i['Engine'] != 'aurora':
                    response3 = client.stop_db_instance(
                        DBInstanceIdentifier=i['DBInstanceIdentifier'])
