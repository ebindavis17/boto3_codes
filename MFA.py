import boto3

client=boto3.client('iam')
sns=boto3.client('sns')

response = client.list_users()
userVirtualMfa = client.list_virtual_mfa_devices()
mfa_users  = []
virtualEnabled = []
physicalString = ''
 
def lambda_handler(event,context):
    for user in response['Users']:
        userMfa = client.list_mfa_devices(UserName=user['UserName'])
        for uname in userMfa['MFADevices']:
            #print(uname)
            virtualEnabled.append(uname['UserName'])
            #print(virtualEnabled) 
            
           
        if len(userMfa['MFADevices']) == 0 :
            if user['UserName'] not in virtualEnabled:
                mfa_users.append(user['UserName'])
                #print(mfa_users)
        
        if len(mfa_users) > 0 :
            physicalString='These users in aab-eng1 is not activated MFA device yet:  \n\n ' + '\n'.join(mfa_users)
        else:
            physicalString='All users are enabled'
            
    response1 = sns.publish(
        TopicArn='******',
        Message=physicalString,
        Subject='List of users with no MFA Device activated') 
    
