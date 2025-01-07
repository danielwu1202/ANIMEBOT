from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 初始化 Flask 應用
app = Flask(__name__)

# Line Bot API 和 Webhook Handler 初始化
LINE_CHANNEL_ACCESS_TOKEN = 'bNmJeiAzOgqF+lva1GofLFs52qHOuRVAntqO4Qt/CnY32ImJ3yq7558nR2H4OwHJXJTqNrNslzW2r2kiPRSxU2NPhyVgnsCdSgQoraFd/hAzz7+9yf3Z1wEsWm9fUmRWeqbeVy60Kzjr/AxXa9rO2AdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'cf474f269c00a7520590347a8f46ba28'
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# Webhook 路徑，用來接收 Line 平台的事件
@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求是否合法
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
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
    app.run(port=8000)
