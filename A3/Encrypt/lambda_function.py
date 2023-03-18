import json
import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def lambda_handler(event, context):

    message = event["message"]

    with open("publicKey.txt","rb") as file:
        publicKey = file.read()

    message = str.encode(message)

    RSApublicKey = RSA.importKey(publicKey)
    OAEP_cipher = PKCS1_OAEP.new(RSApublicKey)
    encryptedMsg = OAEP_cipher.encrypt(message)

    print('Encrypted text:', encryptedMsg)

    encryptedMsg = base64.b64encode(encryptedMsg)


    return {
        "response" : encryptedMsg
    }
