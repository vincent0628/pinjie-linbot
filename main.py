from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)
# LINE BOT info
# line_bot_api = LineBotApi('Channel Access token')
# handler = WebhookHandler('Channel Secret')
# https://developers.line.biz/console/channel/1657173822/basics
line_bot_api = LineBotApi('UaJRv37TED6+8jbkQuZkF4xq+iaadWGtQmBQiUAuCcX4r0UgCCU9F/vKyjCuu/c2mJEt2mCPkkKdEor7FHn07A0cdB5rQYhpczjh34hc8OkfVSrXdmrA75pQ/FY92yjfNA2nG0/Zk5RHbaoYUPrmJwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f0cec20f2bb7c55670631777fb606b28')


@app.route("/callback", methods=['POST'])
def callback():
    # signature是LINE官方提供用來檢查該訊息是否透過LINE官方APP傳送
    signature = request.headers['X-Line-Signature']
    # body就是用戶傳送的訊息，並且是以JSON的格式傳送
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    if message == "愛你":
        message = "愛你一萬年"
    line_bot_api.reply_message(reply_token, TextSendMessage(text = message))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)