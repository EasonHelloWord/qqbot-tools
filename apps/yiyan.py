import requests
from json import loads as json_loads
def yiyan():# 读取一言
    data = requests.get("https://v1.hitokoto.cn").text
    data = json_loads(data)
    if data.get('from_who'):
        sfrom = data.get('from_who')
    else:
        sfrom = data.get('from')
    mes = f"{data.get('hitokoto')}   ——{sfrom}"
    return(mes)
if __name__ == "__main__":
    mes = yiyan()
    print(mes)