import boto3

dbmultiAZ=[]


client = boto3.client('rds')

def lambda_handler(event,context):
  
  response = client.describe_db_instances()
  for i in response['DBInstances']:
      
#      if i['MultiAZ'] == True:
          #print(i['DBInstanceIdentifier'])
          dbmultiAZ.append(i['DBInstanceIdentifier'])
          
'''  
  for rdsinstances in dbmultiAZ:
      response1 = client.modify_db_instance(
          DBInstanceIdentifier=rdsinstances,
          ApplyImmediately=True,
          MultiAZ=False
          )
'''          

   response1 = client.stop_db_instance(
     DBInstanceIdentifier= dbmultiAZ
     )
  
 
