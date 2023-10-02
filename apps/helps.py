import os
import json
if not os.path.exists("helps"):  # 创建hollow目录
    os.mkdir("helps")
if not os.path.exists("helps/list.json"):
    # 如果文件不存在，创建一个空的JSON对象
    data = {}
    # 将JSON对象写入文件
    with open("helps/list.json", "w") as json_file:
        json.dump(data, json_file)
example = {"name": "",
           "version": "",
           "introduction": "",
           "usage": ["",""],
           "example": ""}
with open("helps/list.json", 'r') as file:
        lists = json.load(file)

for list_name in lists:
    if not os.path.exists(f"helps/{list_name}.json"):
        with open(f"helps/{list_name}.json", "w") as json_file:
            json.dump(example, json_file, ensure_ascii=False,indent=4)
def find_and_read_file(string):
    with open("helps/list.json", 'r') as file:
        lists = json.load(file)

    for list_name, list_items in lists.items():
        if string in list_items:
            file_path = os.path.join("helps", f"{list_name}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as json_data:
                    json_data = json.load(json_data)
                    # 格式化为便于阅读的字符串
                    formatted_string = f"名字：{json_data['name']}\n"
                    formatted_string += f"版本：{json_data['version']}\n"
                    formatted_string += f"简介：{json_data['introduction']}\n"
                    formatted_string += "用法：\n"
                    for index, item in enumerate(json_data['usage'], start=1):
                        formatted_string += f"{index}、{item}\n"
                    formatted_string += f"示例：{json_data['example']}"
                    return formatted_string
    return "暂时没有帮助文档呢"

def read_all_file():
    with open("helps/list.json", 'r') as file:
        lists = json.load(file)
    if lists:
        formatted_string = ""
        for list_name in lists:
            file_path = os.path.join("helps", f"{list_name}.json")
            if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as json_data:
                        json_data = json.load(json_data)
                        formatted_string += f"{json_data['name']}    {json_data['introduction']}"
                        if list_name != list(lists.keys())[-1]:
                            formatted_string += "\n"
        return formatted_string
    return "暂时没有帮助文档呢"
    