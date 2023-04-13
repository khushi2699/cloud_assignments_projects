import json
import boto3
from boto3.dynamodb.conditions import Attr
import smtplib
from email.mime.text import MIMEText



dynamodb = boto3.resource('dynamodb') # get the DynamoDB resource
sns = boto3.client('sns')
table = dynamodb.Table('post_details')
table1 = dynamodb.Table('user_details')
client = boto3.client('cognito-idp')
def lambda_handler(event, context):
    
    token = event['token']
    response = client.get_user(
        AccessToken=token
    )
    sendToEmail = response['UserAttributes'][2]['Value']
    postID = event['postID']
    print(sendToEmail)
    print(postID)
    
    index_name = 'email-index'
    
    post_details = table.get_item(
            Key={"postID":postID}
    )
    
    post_owner_email = post_details['Item']['email']
    print(post_owner_email)
    response = table1.scan(
        IndexName=index_name,
        FilterExpression=Attr('email').eq(post_owner_email)
    )
    
    
    print(response)
    
    # response_sns = sns.subscribe(
    #     TopicArn = 'arn:aws:sns:us-east-1:945919196866:Notify',
    #     Protocol = 'email',
    #     Endpoint = sendToEmail
    # )
    
    firstName = response['Items'][0]['firstName']
    lastName = response['Items'][0]['lastName']
    phoneNumber = response['Items'][0]['phoneNumber']
    
    message_body = 'Hello '+sendToEmail+', You showed interest in a post, here are the details of the post owner. Name: '+firstName+' '+lastName+' Contact Number: '+ phoneNumber
    print(message_body)
    
    # response_sns_publish = sns.publish(
    #     TopicArn = 'arn:aws:sns:us-east-1:945919196866:Notify',
    #     Message= message
    # )
    
    
    sender = 'khshah2699@gmail.com'
    recipient = sendToEmail
    subject = 'New Interest Information'
    # message = f"""\
    # From: {sender}
    # To: {recipient}
    # Subject: {subject}
    # Body:
    # {message_body}
    # """
    # TODO implement
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'khshah2699@gmail.com'
    smtp_password = 'cklupnkfkmtqcdev'
    
    msg = MIMEText(message_body)

    # Set the headers of the email
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    try:
        smtp_server = smtplib.SMTP(smtp_server, smtp_port)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(smtp_username, smtp_password)
        smtp_server.sendmail(sender, recipient, msg.as_string())
        print("Email sent successfully")
    except Exception as ex:
        print("Error sending email: ", str(ex))
    finally:
        smtp_server.quit()
        
    return {
        'statusCode': 200,
        'response': 'Email send successfully'
    }
