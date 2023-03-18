import json
import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def lambda_handler(event, context):

    message = event['message']

    with open("privateKey.txt","rb") as file:
        privateKey = file.read()

    message = str.encode(message)

    decryptedMsg = base64.b64decode(message)

    RSAprivateKey = RSA.importKey(privateKey)
    OAEP_cipher = PKCS1_OAEP.new(RSAprivateKey)
    decryptedMsg = OAEP_cipher.decrypt(decryptedMsg)

    return {
        "response" : decryptedMsg
    }
