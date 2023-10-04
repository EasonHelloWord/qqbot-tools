from flask import Flask, request
from apps import repeat,yiyan,EchoCave,config,helps,cqhttp_tools

app = Flask(__name__)

@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    receive(data)
    return ('200')

# 接受消息
def receive(data):
    if data.get('post_type') == 'message':
        print(data)
        message_type = data.get('message_type')
        message = data.get('message')
        if message.startswith("."):
            data['message'] = data.get('message')[1:]
            receive_message(data)
        if message_type == 'private':
            receive_message(data)

# 使用模块
def receive_message(data):
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
    if "type=flash" in message:# 闪照破解
        pass
    # repeat_(data) #复读机 仅用作测试

# 一言
def yiyan_(data): 
    message = yiyan.yiyan()
    cqhttp_tools.send_message(data,message)

#复读机 仅用作测试
def repeat_(data): 
    message = repeat.repeat(data.get('message'))
    cqhttp_tools.send_message(data,message)

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
    cqhttp_tools.send_message(data,message)

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
        
    cqhttp_tools.send_message(data,message)

def helps_(data):
    if not data.get("message"):
        msg = helps.read_all_file()
        print(msg)
    else:
        msg = helps.find_and_read_file(data.get("message"))
    cqhttp_tools.send_message(data, msg)




if __name__ == '__main__':
    app.run('127.0.0.1', 5701, True)