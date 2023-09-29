import os, time, random, json
if not os.path.exists("EchoCave"):  # 创建hollow目录
    os.mkdir("EchoCave")

def EchoCave(msg, user_id):
    if msg:
        msg = msg.replace("\r\n", "\r")  # 将换行符统一为 "\r"
        name = time.strftime("EchoCave/%Y-%m-%d.%H-%M-%S.json")  # 使用绝对路径生成文件名
        message = {
            "msg": msg,
            "user_id": user_id,
            'time': time.strftime("%Y-%m-%d.%H-%M-%S")
        }
        with open(name, "a", encoding='utf-8') as f:
            json.dump(message, f, ensure_ascii=False,indent=4)  # 写入消息到 JSON 文件
        return "你的声音会在这里回响"
    else: return "保存失败，输入为空"
def readfile():
    
    file_name_list = os.listdir('EchoCave')  # 获取 "树洞" 目录下的所有文件名

    if (not file_name_list) or len(file_name_list) == 1:
        return None  # 处理树洞为空的情况

    random_file = random.choice(file_name_list)
    file_path = os.path.join('EchoCave', random_file)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return f"{data.get('msg')}"  # 返回格式化的回复消息
