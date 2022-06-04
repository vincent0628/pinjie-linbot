from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os

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
    text = message = event.message.text
    emoji = None
    if message == "愛你":
        text = "愛你一萬年"
    elif message == "你愛我嗎":
        text = "愛你愛你 愛你一萬年!!!\U00002665\U00002665\U00002665"
    elif message in ["交往", "紀念日", "交往紀念日"]:
        text = "交往紀念日是0722 \n \
            以下 是 $文森$送你的 五個禮物 \n \
            1. https://chunjie100.netlify.app/$\n \
            2. https://pinjie2020.netlify.app/ \n \
            3. https://pinjie-xmas2020.netlify.app/\n \
            4. https://vincent0628.github.io/pinjie_2021_0722/\n \
            5. https://vincent0628.github.io/pinjie_2022_0214/\n \
            "
        emoji = [
            {"index": 22, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "204"},
            {"index": 25, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "204"},
            {"index": 75, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "047"},
        ]

    line_bot_api.reply_message(reply_token, TextSendMessage(text=text, emojis=emoji))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)