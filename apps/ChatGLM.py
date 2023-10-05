from apps import config
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
model = model.eval()

def ChatGlm(data):# ai聊天
    history = config.get_config(data).get("ai_temp")
    if not history:
        history = []
    response, history = model.chat(tokenizer,data.get("message"), history=history)
    if len(history) > 4:
        history = history[-4:]
    config.set_config(data,"ai_temp",history)
    return response