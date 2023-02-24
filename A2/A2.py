import boto3
from flask import Flask, request, jsonify, Response

app = Flask(__name__)


@app.route('/storedata', methods=['GET', 'POST'])
def storedata_function():
    print("Start store data")
    json_data = request.get_json()
    data = json_data.get('data')
    session = boto3.Session(
        aws_access_key_id = "ASIA5YPJNP3BMWVSNFWC",
        aws_secret_access_key = "go69jHxC/NssL5ZoSqjagzN8z9QKh/7B0TBF5bmv",
        aws_session_token = "FwoGZXIvYXdzEH4aDJ0zjjpk3pFNcvLJEiLAASifzNHhu+zaQ9mLBRXVliRGuSplBIAZIu9nO+Npm1Z6RbUwxEysm9NCCrb2vIuz6mvKG1xasjRCnBphh9SmlXfbazM4bOoVqtnpZo5l4ZSRyaK/jnWS2dpfkjpzB8V6Xid43dp40x1MtGSFgkPnBofpxg4SVZg7L7Gh0NEG4GayYnUWWSySqHifHtZfRBTWXDRZiIMe+UGHBZ6Xn4043/rbk6QNg7mUmMHGikUxocGHEgOBDin7OXonDP6fUoBvRyjw0OKfBjIt0zreOhujKkAHS59300ch2PfBA9l/Gs+A7CsBg/JhBymBJU/bN23t2Q8Z6/lc",
        region_name = 'us-east-1'
    )
    s3 = session.resource('s3')
    file_name = 'data.txt'
    bucket_name = 'a2-b00923816'
    try:
        s3.head_object(Bucket=bucket_name, Key=file_name)
        print('File already exists in S3 bucket.')

    except:
        s3.Object(bucket_name, file_name).put(Body = data)
        print('File created and uploaded successfully.')
    result = {'s3uri': 'https://a2-b00923816.s3.amazonaws.com/data.txt'}
    print("Store data working")
    return jsonify(result), 200


@app.route('/appenddata', methods=['GET', 'POST'])
def appenddata_function():
    print("Start append data")
    json_data = request.get_json()
    data = json_data.get('data')
    session = boto3.Session(
        aws_access_key_id = "ASIA5YPJNP3BMWVSNFWC",
        aws_secret_access_key = "go69jHxC/NssL5ZoSqjagzN8z9QKh/7B0TBF5bmv",
        aws_session_token = "FwoGZXIvYXdzEH4aDJ0zjjpk3pFNcvLJEiLAASifzNHhu+zaQ9mLBRXVliRGuSplBIAZIu9nO+Npm1Z6RbUwxEysm9NCCrb2vIuz6mvKG1xasjRCnBphh9SmlXfbazM4bOoVqtnpZo5l4ZSRyaK/jnWS2dpfkjpzB8V6Xid43dp40x1MtGSFgkPnBofpxg4SVZg7L7Gh0NEG4GayYnUWWSySqHifHtZfRBTWXDRZiIMe+UGHBZ6Xn4043/rbk6QNg7mUmMHGikUxocGHEgOBDin7OXonDP6fUoBvRyjw0OKfBjIt0zreOhujKkAHS59300ch2PfBA9l/Gs+A7CsBg/JhBymBJU/bN23t2Q8Z6/lc",
        region_name = 'us-east-1'
    )
    s3 = session.resource('s3')
    file_name = 'data.txt'
    bucket_name = 'a2-b00923816'
    s3.Object(bucket_name, file_name).load()
    existing_data = s3.Object(bucket_name, file_name).get()['Body'].read().decode('utf-8')
    appended_data = existing_data + data
    s3.Object(bucket_name, file_name).put(Body=appended_data)
    print("Append data working")
    response = Response(status=200)
    return response


@app.route('/deletefile', methods=['GET', 'POST'])
def deletefile_function():
    print("Start delete data")
    json_data = request.get_json()
    data = json_data.get('s3uri')  # data = https://a2-b00923816.s3.amazonaws.com/data.txt
    session = boto3.Session(
        aws_access_key_id = "ASIA5YPJNP3BMWVSNFWC",
        aws_secret_access_key = "go69jHxC/NssL5ZoSqjagzN8z9QKh/7B0TBF5bmv",
        aws_session_token = "FwoGZXIvYXdzEH4aDJ0zjjpk3pFNcvLJEiLAASifzNHhu+zaQ9mLBRXVliRGuSplBIAZIu9nO+Npm1Z6RbUwxEysm9NCCrb2vIuz6mvKG1xasjRCnBphh9SmlXfbazM4bOoVqtnpZo5l4ZSRyaK/jnWS2dpfkjpzB8V6Xid43dp40x1MtGSFgkPnBofpxg4SVZg7L7Gh0NEG4GayYnUWWSySqHifHtZfRBTWXDRZiIMe+UGHBZ6Xn4043/rbk6QNg7mUmMHGikUxocGHEgOBDin7OXonDP6fUoBvRyjw0OKfBjIt0zreOhujKkAHS59300ch2PfBA9l/Gs+A7CsBg/JhBymBJU/bN23t2Q8Z6/lc",
        region_name = 'us-east-1'
    )
    s3 = session.resource('s3')
    bucket_name = data.split('/')[2]
    bucket_name = bucket_name.split('.')[0]
    file_name = data.split('/')[3]
    s3.Object(bucket_name, file_name).delete()
    print('File deleted')
    response = Response(status=200)
    return response


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
