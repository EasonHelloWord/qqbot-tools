import requests
from flask import Flask, request
from apps import repeat,yiyan,EchoCave

app = Flask(__name__)

@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    if data.get('post_type') == 'message':
        receive(data)
    return ('200')

# 接受消息
def receive(data):
    message_type = data.get('message_type')
    message = data.get('message')
    if message_type == 'group' and message.startswith("."):
        data['message'] = data.get('message')[1:]
        tools(data)
    if message_type == 'private':
        tools(data)

# 使用模块
def tools(data):
    message = data.get('message')
    if message.startswith("一言"):# 一言
        yiyan_(data)
    if message.startswith("回声洞"):# 回声洞
        data['message'] = data['message'][3:]
        EchoCave_(data,'write')
    if message == "回声":# 回声
        data['message'] = data['message'][2:]
        EchoCave_(data,'read')
    # repeat_(data) #复读机 仅用作测试

# 一言
def yiyan_(data): 
    message_type = data.get('message_type')
    message = yiyan.yiyan()
    user_id = data.get('user_id',None)
    group_id = data.get('group_id',None)
    send_message(message_type,message,user_id,group_id)

#复读机 仅用作测试
def repeat_(data): 
    message = repeat.repeat(data.get('message'))
    message_type = data.get('message_type')
    user_id = data.get('user_id',None)
    group_id = data.get('group_id',None)
    send_message(message_type,message,user_id,group_id)

#回声洞
def EchoCave_(data,method):
    if method == "read":
        msg = EchoCave.readfile()
        if msg:
            message = "隐约中你听到了一个回声：\n"+msg
        else: message = "这里还很安静"
    if method == "write":
        mes = EchoCave.EchoCave(data['message'],data['user_id'])
        message = mes + "\n"
        msg = EchoCave.readfile()
        if msg:
            message += "隐隐中你听到了一个回声：\n"+msg
        else: message += "这里还很安静"
    message_type = data.get('message_type')
    user_id = data.get('user_id',None)
    group_id = data.get('group_id',None)
    send_message(message_type,message,user_id,group_id)


# 发送消息
def send_message(message_type, message, user_id=None, group_id=None, auto_escape=False):
    data = {
        'message_type': message_type,
        'user_id': user_id,
        'group_id': group_id,
        'message': message,
        'auto_escape': auto_escape
    }
    requests.post("http://127.0.0.1:5700/send_msg", data)

# 发送报文
def post(URL, data):
    requests.post(f"http://127.0.0.1:5700/{URL}", data)

if __name__ == '__main__':
    app.run('127.0.0.1', 5701, True)