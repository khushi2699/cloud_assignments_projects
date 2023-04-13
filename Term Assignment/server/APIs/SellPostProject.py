import json
import boto3

dynamodb = boto3.resource('dynamodb') # get the DynamoDB resource
table = dynamodb.Table('post_details')
client = boto3.client('cognito-idp')
def lambda_handler(event, context):
    
    postID = event['postID']
    
    response = table.update_item(
                Key={'postID': postID},
                UpdateExpression="set issold=:r",
                ExpressionAttributeValues={
                    ':r': 'true'},
                ReturnValues="UPDATED_NEW")    
    return {
        'statusCode': 200,
        'response': response
    }
