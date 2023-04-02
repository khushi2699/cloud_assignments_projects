import json
import boto3


def lambda_handler(event, context):
    # TODO implement
    message = event['type']
    sqs = boto3.client('sqs')

    if message == 'CONNECT':
        # Receive messages from the queue
        queue_url = 'https://sqs.us-east-1.amazonaws.com/945919196866/Contect_Queue'
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=0
        )

        for message in response['Messages']:
            # Get the message body
            message_body = message['Body']
            message_json = json.loads(message_body)
            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            result = { "type" : "CONNACK", "returnCode": 0, "username": message_json['username'], "password": message_json['password'] }
            return result

    elif message == 'SUBSCRIBE':
        # Receive messages from the queue
        queue_url = 'https://sqs.us-east-1.amazonaws.com/945919196866/Subscribe_Queue'
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=0
        )

        for message in response['Messages']:
            # Get the message body
            message_body = message['Body']
            message_json = json.loads(message_body)
            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            result = { "type" : "SUBACK" , "returnCode": 0 }
            return result

    elif message == 'PUBLISH':
        # Receive messages from the queue
        queue_url = 'https://sqs.us-east-1.amazonaws.com/945919196866/Publish_Queue'
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=0
        )

        for message in response['Messages']:
            # Get the message body
            message_body = message['Body']
            message_json = json.loads(message_body)
            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            result = { "type" : "PUBACK" , "returnCode": 0, "payload": { "key": message_json['payload']['key'], "value": message_json['payload']['value'] } }
            return result


