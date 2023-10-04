import os
import json
from apps.cqhttp_tools import get_admin_user_ids

CONFIG_DIR = "configs"  # 将配置目录名更改为英文

if not os.path.exists(CONFIG_DIR):
    os.mkdir(CONFIG_DIR)

def get_config(data):
    type = data.get('message_type')
    if type == 'group':
        uid = data.get("group_id")
    if type == 'private':
        uid = data.get("user_id")
    if data.get("notice_type") == "group_recall":
        type = "group"
        uid = data.get("group_id")
    filename = os.path.join(CONFIG_DIR, f"{type}_{uid}.json")
    try:
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data

def set_config(data, name, detail):
    type = data.get('message_type')
    if type == 'group':
        uid = data.get("group_id")
        admin_list = get_admin_user_ids(data)
        if not data.get('user_id') in admin_list:
            return "权限不足"
    if type == 'private':
        uid = data.get("user_id")
    filename = os.path.join(CONFIG_DIR, f"{type}_{uid}.json")

    try:
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    if not detail:
        try:
            del data[name]
        except:
            mes = f"未找到配置{name}，他可能已经被删除"
        else:
            mes = f"配置{name}已删除"
    else:
        data[name] = detail
        mes = f"设置成功~'{name}'的值为'{detail}'"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return mes
