import hashlib
from flask import Flask,request,jsonify
app = Flask(__name__)
@app.route('/' , methods = ['POST'])
def index():
    data = request.get_json()['data']
    print(data)
    with open('/users/tmp/'+data, "rb") as f:
        content = f.read()
        return jsonify({"checksum": hashlib.md5(content).hexdigest(), "file": data})

if __name__ == "__main__":
  app.run(debug=True, port=5001, host='0.0.0.0')