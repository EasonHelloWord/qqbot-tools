import requests,json,os
filename = os.path.join("config.json")
with open(filename, encoding="utf-8") as f:
    config_data = json.load(f)

def get_group_member_list(data): # 获取群成员信息
    if data.get('message_type') == "group":
        data_send = {"group_id":data.get("group_id")}
        back = post("get_group_member_list",data_send)
        back = json.loads(back)
    else:
        back = ""
    return back

def get_admin_user_ids(data):# 获取管理员列表
    if data.get("message_type") == "group":
        data_back = get_group_member_list(data)
        admin_user_ids = [entry["user_id"] for entry in data_back["data"] if entry["role"] == "admin" or entry["role"] == "owner"]
        return admin_user_ids
    return None

def get_group_member_info(data,user_id=None):# 获取群成员信息
    if user_id:
        user_id = user_id
    else:
        user_id = data.get('user_id',None)
    group_id = data.get('group_id',None)
    datas = {
        'user_id': user_id,
        'group_id': group_id,
    }
    return json.loads(post("get_group_member_info", datas))

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
    return post("send_msg", data)

def get_msg(message_id):# 获取消息
    datas = {
        'message_id': message_id
    }
    return post("get_msg",datas)

def get_login_info():# 获取登录号信息
    mes = json.loads(post("get_login_info"))
    return mes

# 发送报文
def post(URL, data=None):
    return requests.post(f"{config_data['cqhttp_address']}{URL}", data).text


if __name__ == "__main__":
    data = {'message_type':"group","group_id":'123456'}
    data_back = get_group_member_list(data)
    admin_user_ids = [entry["user_id"] for entry in data_back["data"] if entry["role"] == "admin"]
    print(admin_user_ids)