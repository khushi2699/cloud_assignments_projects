import boto3
import json
dynamodb = boto3.resource('dynamodb') # get the DynamoDB resource
table = dynamodb.Table('user_details')
client = boto3.client('cognito-idp')
sm = boto3.client('secretsmanager')
def lambda_handler(event, context):
    
    secret_name = "CloudSecret"
    response = sm.get_secret_value(SecretId=secret_name)
    secret_value = json.loads(response['SecretString'])
    clientID = secret_value['ClientPoolID']
    print(clientID)
    password = event["password"]
    email = event["email"]

    try: 
        response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': email,
            'PASSWORD': password,
        },
        ClientId=clientID,
        )

        if response:
            print(response['AuthenticationResult']['AccessToken'])
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": "true",
                },
                'jwt_token': response
            }
    except Exception as e:
        exception_type = e.__class__.__name__
        exception_message = str(e)
        
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",                
            },
            'jwt_token': 'null',
            'response': exception_message
        }
        
        
    # response = client.get_user(
    #     AccessToken='eyJraWQiOiJ4VjhPSVlXZnlCazJqTHBwOEN6eGw4RkJTanlaVW42dGxWSEJXY1RIN1k0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI5YjY5MDA4Yy1iYjAyLTRjNzYtODgyYi1hZjk4MTk2NWE4NjEiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9jMXlwdk1WdFciLCJjbGllbnRfaWQiOiIxaWtqZXAyM2k3ZWw4NDJhNGIyZm1yZXIzOSIsIm9yaWdpbl9qdGkiOiIyNTJiNDlhYy0wOWMyLTRmYWQtOWRjZi0wMTJiN2ViZGZjYTgiLCJldmVudF9pZCI6IjIwMWU3M2VlLTdhZmUtNDgyMS1iMTgzLTI1MzJjYWYxMDk0ZiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2ODA5MjkxNTAsImV4cCI6MTY4MDkyOTQ1MCwiaWF0IjoxNjgwOTI5MTUwLCJqdGkiOiJmMTJhYzg4NC1lNGRjLTQ2MGYtOTJmMS05NmRkM2I5MTE4NDMiLCJ1c2VybmFtZSI6IjliNjkwMDhjLWJiMDItNGM3Ni04ODJiLWFmOTgxOTY1YTg2MSJ9.xZt7auuxtTfzuzU3EY4oSn2U4EaR_zyO2kqIY8AnnZIxpnDc7HBDMdetZ9pYVa2EOkLLWADnKKQiy4_uwsE90DjWKkOLOdWVMGQz0Nql-deyAwL_5AMRNIW5SAyTpC1sjjJBR5j_Yj-SSZ3zmBG25xcXxVGIDy09dHvy4SCy-n2yEETAcSMU1i8RpfK4eC90ORXWUIObAyEhngEDIKXHylk3mtRNjJzQ7SG_zMTyMStCAu1TdJCNcswPpLmjhLwgV0z_q09lt-etIODuYqX7ZXlTj8PndvsRt8ajDbV7Oa7X_ooFlr9NOVGyF5ZEGE0eGBY0izrGD1AhgD98hBihBw'
    # )
