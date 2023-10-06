from flask import Flask, request
from apps import repeat,yiyan,EchoCave,config,helps,cqhttp_tools,flash,group_recall
import threading, os, json
app = Flask(__name__)

@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    receive(data)
    return ('200')

# 接受消息
def receive(data):
    if data.get('post_type') == 'message':
        # print(data)
        message_type = data.get('message_type')
        message = data.get('message')
        if message.startswith("."):
            data['message'] = data.get('message')[1:]
            receive_message(data)
            return ""
        if message_type == 'private':
            receive_message(data)
            return ""
    if data.get('post_type') == 'notice':
        receive_notice(data)
    return ""

# 使用模块
def receive_message(data):
    message = data.get('message')
    if message.startswith("一言"):# 一言
        yiyan_(data)
        return ""
    if message.startswith("回声洞"):# 回声洞
        data['message'] = data['message'][3:]
        EchoCave_(data,'write')
        return ""
    if message == "回声":# 回声
        data['message'] = data['message'][2:]
        EchoCave_(data,'read')
        return ""
    if message.startswith("配置"):# 配置
        data['message'] = data['message'][2:]
        config_(data)
        return ""
    if message.startswith("帮助"):# 帮助
        data['message'] = data['message'][2:]
        helps_(data)
        return ""
    if "type=flash" in message:# 闪照破解
        flash_(data)
        return ""
    if message.lower().startswith("ai"):# ai
        data['message'] = data['message'][2:]
        threading.Thread(target=ChatGlm_, args=(data,)).start()
        return ""
    # repeat_(data) #复读机 仅用作测试


def receive_notice(data):
    if data.get("notice_type") == 'group_recall':# 群消息撤回
        group_recall_(data)
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
        if config_data.get("ai_temp"):
            del config_data["ai_temp"]
        message = ""
        for key, value in config_data.items():
            message += f"{key}: {value}"
            if key != list(config_data.keys())[-1]:
                message += "\n"
        if not message:
            message = "还没有配置过任何东西哦"
    else:
        name_and_detail = []
        for part in data.get("message").split(":"):
            for x in part.split("："):
                name_and_detail.append(x)
        if len(name_and_detail) == 1:
            name_and_detail.append("")
        message = config.set_config(data,name_and_detail[0],name_and_detail[1])
        
    cqhttp_tools.send_message(data,message)

# 帮助文档
def helps_(data):
    if not data.get("message"):
        msg = helps.read_all_file()
    else:
        msg = helps.find_and_read_file(data.get("message"))
    cqhttp_tools.send_message(data, msg)

# 闪照
def flash_(data):
    message = flash.flash(data)
    if message:
        message = f"成功破解[{data.get('sender').get('nickname')}]的闪照：\n{message}"
        cqhttp_tools.send_message(data,message)

def group_recall_(data):
    mes = group_recall.group_recall(data)
    if mes:
        data = {
        'message_type': "group",
        'user_id': data.get("user_id"),
        'group_id': data.get("group_id"),
        }
        cqhttp_tools.send_message(data,mes[0])
        cqhttp_tools.send_message(data,mes[1])

def ChatGlm_(data):# ai
    if config_data["enable_ai"]:
        cqhttp_tools.send_message(data,"机器人性能较弱，回复时间可能较长，请耐心等待。")
        try:mes = ChatGLM.ChatGlm(data)
        except:mes = '抛出异常：我的电脑跑不动这个模型啦！（悲）'
        cqhttp_tools.send_message(data,mes)
    else:cqhttp_tools.send_message(data,"功能未启动")

if __name__ == '__main__':
    # 读取配置文件
    filename = os.path.join("config.json")
    try:
        with open(filename, encoding="utf-8") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        config_data = {"enable_ai":False}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
    except: print("配置文件异常")
    if config_data["enable_ai"]:
        from apps import ChatGLM
    app.run('127.0.0.1', 5701, False)