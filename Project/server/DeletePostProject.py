import json
import boto3

dynamodb = boto3.resource('dynamodb') # get the DynamoDB resource
table = dynamodb.Table('post_details')
client = boto3.client('cognito-idp')
def lambda_handler(event, context):
    
    postID = event['postID']
    
    response = table.delete_item(Key = {
        'postID': postID
    })
    # TODO implement
    return {
        'statusCode': 200,
        'response': response
    }
