import requests,json

def get_group_member_list(data): # 获取群成员信息
    if data.get('message_type') == "group":
        data_send = {"group_id":data.get("group_id")}
        back = post("get_group_member_list",data_send).text
        back = json.loads(back)
    else:
        back = ""
    return back

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
    return requests.post("http://127.0.0.1:5700/send_msg", data)


# 发送报文
def post(URL, data):
    return requests.post(f"http://127.0.0.1:5700/{URL}", data)


if __name__ == "__main__":
    data = {'message_type':"group","group_id":'123456'}
    data_back = get_group_member_list(data)
    admin_user_ids = [entry["user_id"] for entry in data_back["data"] if entry["role"] == "admin"]
    print(admin_user_ids)