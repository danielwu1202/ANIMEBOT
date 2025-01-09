import os

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from animebot import anime_crawler

# 初始化 Flask 應用
app = Flask(__name__)

# Line Bot API 和 Webhook Handler 初始化
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


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
    user_message = event.message.text

    if user_message == '動畫':
        anime_info = anime_crawler()

        reply = ''

        for anime in anime_info:
            reply += f"動畫名稱：{anime[0]}\n"
            reply += f"動畫集數：{anime[1]}\n"
            reply += f"動畫年份：{anime[2]}\n"
            reply += f"動畫網址：{anime[3]}\n"
            reply += f"下架日期：{anime[4]}\n\n"

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render 分配的埠號，預設值為 8000
    app.run(host="0.0.0.0", port=port)  # 監聽所有外部請求
