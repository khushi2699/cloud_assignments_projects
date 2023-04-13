import json
import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb') # get the DynamoDB resource
table = dynamodb.Table('post_details')
client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    index_name = 'email-index'

    token = event['token']
    response = client.get_user(
        AccessToken=token
    )
    
    
    email = response['UserAttributes'][2]['Value']
    response = table.scan(
        IndexName=index_name,
        FilterExpression=Attr('email').ne(email) & Attr('issold').eq('false')
    )
    items = response['Items']
    # TODO implement
    return {
        'statusCode': 200,
        'items': items,
    }
