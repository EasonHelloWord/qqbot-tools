from apps.config import get_config

def flash(data):
    if get_config(data).get("ban_flash",'False').lower() == "true":
        message = data.get("message")
        pic = f"{message[:-12]}]"
        return pic
    return None