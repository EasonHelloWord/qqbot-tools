import requests
from flask import Flask, request
from apps import repeat,yiyan,EchoCave,config,helps

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
    if message.startswith("配置"):# 配置
        data['message'] = data['message'][2:]
        config_(data)
    if message.startswith("帮助"):# 帮助
        data['message'] = data['message'][2:]
        helps_(data)
    # repeat_(data) #复读机 仅用作测试

# 一言
def yiyan_(data): 
    message = yiyan.yiyan()
    send_message(data,message)

#复读机 仅用作测试
def repeat_(data): 
    message = repeat.repeat(data.get('message'))
    send_message(data,message)

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
    send_message(data,message)

# 配置
def config_(data):
    if not data.get("message"):
        config_data = config.get_config(data)
        message = ""
        for key, value in config_data.items():
            message += f"{key}: {value}"
            if key != list(config_data.keys())[-1]:
                message += "\n"
        if not message:
            message = "还没有配置过任何东西哦"
    else:
        name_and_detail = data.get("message").split(":")
        if len(name_and_detail) == 1:
            name_and_detail[1] = ""
        message = config.set_config(data,name_and_detail[0],name_and_detail[1])
        
    send_message(data,message)

def helps_(data):
    if not data.get("message"):
        msg = helps.read_all_file()
        print(msg)
    else:
        msg = helps.find_and_read_file(data.get("message"))
    send_message(data, msg)
# 发送消息
def send_message(data, message, auto_escape=False):
    message_type = data.get('message_type')
    user_id = data.get('user_id',None)
    group_id = data.get('group_id',None)
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