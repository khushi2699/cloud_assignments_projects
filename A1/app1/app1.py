import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/checksum', methods=['POST'])
def home():
    data = request.get_json()
    name = data.get('file')
    if name:
        file_path = os.path.join('/users/tmp/' + name)
        if os.path.exists(file_path):
            data1 = name
            response = requests.post('http://app2:5001/', json={'data': data1})
            return response.json()
        else:
            return jsonify({"error": "File not found", "file": name})
    else:
        return jsonify({"error": "Invalid JSON input.", "file": print("null")})

if __name__ == "__main__":
  app.run()
