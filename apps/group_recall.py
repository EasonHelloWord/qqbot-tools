from apps.cqhttp_tools import get_login_info,get_group_member_info,get_msg
from apps.config import get_config
import json
def group_recall(data):# 撤回消息破解
    if get_config(data).get("ban_recall",'False').lower() == "true":
        if data.get("user_id") != get_login_info().get('data').get('user_id'):
            if data.get("user_id") == data.get("operator_id"):
                user_nickname = get_group_member_info(data,user_id=data.get("user_id")).get('data').get('nickname')
                mes1 = f"{user_nickname}撤回了一条消息"
                
            else:
                user_nickname = get_group_member_info(data,user_id=data.get("user_id")).get('data').get('nickname')
                operator_nickname = get_group_member_info(data,user_id=data.get("operator_id")).get('data').get('nickname')
                mes1 = f"{operator_nickname}撤回了{user_nickname}的一条消息"
            
            msg = get_msg(data.get("message_id"))
            # 找到JSON部分并解析
            json_start = msg.find("{")
            json_end = msg.rfind("}") + 1
            json_data = msg[json_start:json_end]

            # 解析JSON数据
            try:
                data_dict = json.loads(json_data)
                # 提取message字段
                message_value = data_dict.get("data").get("message")
                
                if not message_value:
                    message_value = "破译失败，内容不受支持"
            except json.JSONDecodeError as e:
                print("JSON解析错误:", str(e))
            mes2 = f"{message_value}"
            return [mes1,mes2]
    return None