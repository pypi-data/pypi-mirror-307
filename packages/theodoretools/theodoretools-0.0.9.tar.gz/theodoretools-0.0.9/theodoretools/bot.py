import os
import requests

def feishu_text(message: str):
    feishu_hook = os.getenv("FEISHU_HOOK")
    if not feishu_hook:
        raise ValueError("FEISHU_HOOK is not set")
    
    token = feishu_hook.replace('https://open.feishu.cn/open-apis/bot/v2/hook/', '')
    url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{token}"

    response = requests.post(
        url,
        json={
            "msg_type": "text",
            "content": {
                "text": message
            }
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    return response.json()
