import boto3

dynamodb = boto3.resource('dynamodb') # get the DynamoDB resource
table = dynamodb.Table('user_details') 
client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    bannerID = event["bannerID"]
    firstName = event["firstName"]
    lastName = event["lastName"]
    password = event["password"]
    email = event["email"]
    phoneNumber = event["prefix"]+event["phone"]
    
    input = {
        "BannerId": bannerID,
        "firstName": firstName,
        "lastName": lastName,
        "password": password,
        "email": email,
        "phoneNumber": phoneNumber
    }
    banner_response = table.query(
        KeyConditionExpression='BannerId = :bannerID',
        ExpressionAttributeValues={
            ':bannerID': bannerID
        }
    )
    email_response = table.query(
        IndexName='email-index',
        KeyConditionExpression='email = :email',
        ExpressionAttributeValues={
            ':email': email
        }
    )
    
    bannerId_exist = banner_response['ScannedCount']
    email_exist = email_response['ScannedCount']
    

    if bannerId_exist == 0 and email_exist == 0:
        response_cognito = client.sign_up(
            ClientId='1ikjep23i7el842a4b2fmrer39',
            Username=email,
            Password=password,
        )
        response_dynamo = table.put_item(Item=input)    # Add item to table
        return {
            'statusCode': 200,
            'headers': {
              "Access-Control-Allow-Origin": "*", 
              "Access-Control-Allow-Credentials": "true",
              "Access-Control-Allow-Headers": "Content-Type",
              "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            'result_cognito': response_cognito,
            'result_dynamo': response_dynamo
        }
    else:
        if bannerId_exist != 0: 
            return {
                'statusCode': 400,
                'headers': {
                  "Access-Control-Allow-Origin": "*", 
                  "Access-Control-Allow-Credentials": "true",
                },            
                'result': 'Banner ID Already Exist. It must be unique',
            }
        if email_exist != 0:
            return {
                'statusCode': 400,
                'headers': {
                  "Access-Control-Allow-Origin": "*", 
                  "Access-Control-Allow-Credentials": "true",
                },            
                'result': 'Email Address Already Exist. It must be unique',

            }
