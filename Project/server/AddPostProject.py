import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb') # get the DynamoDB resource
table = dynamodb.Table('counter_post')
table1 = dynamodb.Table('post_details')
client = boto3.client('cognito-idp')
def lambda_handler(event, context):

    imageUrl = event["imageUrl"]
    token = event["token"]
    values = event["fieldValues"]
        
    print(imageUrl)
    print(token)
    print(values)
    
    productName = values['productName']
    price = values['price']
    description = values['description']
    category = values['category']
        
    response = client.get_user(
        AccessToken=token
    )
        
    email = response['UserAttributes'][2]['Value']
    
    print(email)
    
    postID = str(uuid.uuid4())
    print(postID)
    
    # count = table.scan()
    # counter = count['Items'][0]['counter_value']
    # counter = counter + 1
    
    # print(count)
    
    input = {
        "postID": postID,
        "ProductName": productName,
        "Price": price,
        "Description": description,
        "email": email,
        "url": imageUrl,
        "category": category,
        "issold": 'false'
    }
    response_dynamo = table1.put_item(Item=input)    # Add item to table

    # response = table.update_item(
    #             Key={'post_counter': 0},
    #             UpdateExpression="set counter_value=:r",
    #             ExpressionAttributeValues={
    #                 ':r': counter},
    #             ReturnValues="UPDATED_NEW")
    return{
        'statusCode': '200',
        'imageUrl': imageUrl,
        'token': token,
        'values': values
    }
