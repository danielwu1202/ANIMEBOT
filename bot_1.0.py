import os

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

api_key = os.environ.get('KEY')

# 初始化 Flask 應用
app = Flask(__name__)

# Line Bot API 和 Webhook Handler 初始化
LINE_CHANNEL_ACCESS_TOKEN = '你的 Channel Access Token'
LINE_CHANNEL_SECRET = '你的 Channel Secret'
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

print("API KEY", api_key)

print('config')
print(LINE_CHANNEL_ACCESS_TOKEN)
print(LINE_CHANNEL_SECRET)


# Webhook 路徑，用來接收 Line 平台的事件
@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求是否合法
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    print("Request Body:", body)
    print("X-Line-Signature:", signature)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 回應訊息的處理邏輯
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回覆用戶傳來的相同訊息
    reply_text = event.message.text
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render 分配的埠號，預設值為 8000
    app.run(host="0.0.0.0", port=port)  # 監聽所有外部請求
