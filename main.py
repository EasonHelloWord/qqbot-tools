import requests
from flask import Flask, request
from apps import repeat
app = Flask(__name__)
@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    if data.get('post_type') == 'message':
        receive(data)
    return ('200')

def receive(data):
    if data.get('message_type') == 'group' and data.get('message')[0] == ".":
        data['message'] = data.get('message')[1:]
        tools(data)
    if data.get('message_type') == 'private':
        tools(data)

def tools(data):
    repeat_(data)

def repeat_(data):
    message = repeat.main(data.get('message'))
    message_type = data.get('message_type')
    user_id = data.get('user_id',None)
    group_id = data.get('group_id',None)
    send_message(message_type,message,user_id,group_id)

def send_message(message_type,message,user_id=None,group_id=None,auto_escape=False):
    data = {'message_type':message_type,
            'user_id':user_id,
            'group_id':group_id,
            'message':message,
            'auto_escape':auto_escape}
    requests.post(f"http://127.0.0.1:5700/send_msg", data)

def post(URL, data):
    requests.post(f"http://127.0.0.1:5700/{URL}", data)

if __name__ == '__main__':
    app.run('127.0.0.1', 5701, True)