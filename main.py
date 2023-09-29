import requests
from flask import Flask, request
app = Flask(__name__)
@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    if data.get('post_type') == 'message':
        print(data)
        receive(data)
    return ('200')
def receive(data):
    if data.get('message')[0] == ".":
        data['message'] = data.get('message')[1:]
def send(URL, data):
    print('send')
    requests.post(f"http://127.0.0.1:5700/{URL}", data)
if __name__ == '__main__':
    app.run('127.0.0.1', 5701, True)