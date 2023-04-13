import json
import boto3

rekognition_client = boto3.client('rekognition')
def lambda_handler(event, context):
    
    s3_url = event['imageUrl']

    bucket_name, object_key = s3_url.split('//')[1].split('/', 1)
    
    response = rekognition_client.detect_labels(Image={'S3Object': {'Bucket': 'cloudproject2023', 'Name': object_key}})
    
    result = response['Labels'][0]['Name']

    return {
        'statusCode': 200,
        'result': result
    }
