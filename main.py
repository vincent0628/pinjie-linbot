from pathlib import Path
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
import datetime
import random
import pandas
import json 

app = Flask(__name__)
# LINE BOT info
# line_bot_api = LineBotApi('Channel Access token')
# handler = WebhookHandler('Channel Secret')
# https://developers.line.biz/console/channel/1657173822/basics
line_bot_api = LineBotApi('UaJRv37TED6+8jbkQuZkF4xq+iaadWGtQmBQiUAuCcX4r0UgCCU9F/vKyjCuu/c2mJEt2mCPkkKdEor7FHn07A0cdB5rQYhpczjh34hc8OkfVSrXdmrA75pQ/FY92yjfNA2nG0/Zk5RHbaoYUPrmJwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f0cec20f2bb7c55670631777fb606b28')

def get_events(path):
    text = ""
    with open(path, 'r', encoding="utf-8") as f:
        data = json.load(f)
        print(data)
        for key in list(data.keys()):
            text += f"{key}\n"
            for i in range(len(data[key])-1):
                text += f"({i+1}.)"
                text += data[key][i]["Date"]+'\t'
                text += data[key][i]["Name"]
                text += "\n"
            text += "\n"
    print(text)
    return text

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
    interval = datetime.datetime.now() - datetime.datetime(2020, 7, 22)
    if message == "愛你":
        text = "愛你一萬年"
    elif message == "你愛我嗎":
        text = "愛你愛你 愛你一萬年!!!💗💗💗"
    elif message in ["交往", "紀念日", "交往紀念日"]:
        text = '\n'.join([
            '交往紀念日是2020/07/22 $',
            '距離今日'+str(interval.days+1),
            '以下是 $文森$ 送你的 五個禮物',
            '1. https://chunjie100.netlify.app/ ',
            '2. https://pinjie2020.netlify.app/',
            '3. https://pinjie-xmas2020.netlify.app/',
            '4. https://vincent0628.github.io/pinjie_2021_0722/',
            '5. https://vincent0628.github.io/pinjie_2022_0214/',
        ])
        indices = [index for index in range(len(text)) if text.startswith('$', index)]
        emoji = [
            {"index": indices[0], "productId": "5ac21184040ab15980c9b43a", "emojiId": "010"},
            {"index": indices[1], "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "091"},
            {"index": indices[2], "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "091"},
        ]
    elif message == "吃":
        text = get_events('events/foods.json')
    elif message in ["電影", "movie"]:
        text = get_events('events/movies.json')
    elif message in ["玩"]:
        text = get_events('events/play.json')
    elif message in ["抽"]:
        googleSheetId = '1JEbsrURmv9ZTLm-er6mlDH1AywsXho4czELpnujMhkw'
        worksheetName = 'pinjie'
        URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(googleSheetId, worksheetName)
        df = pandas.read_csv(URL)
        image_url_array = df[df.columns[4]].to_numpy()
        image_url = random.choice(image_url_array)
        image_message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        
        line_bot_api.reply_message(reply_token, image_message)
        return

    line_bot_api.reply_message(reply_token, TextSendMessage(text=text, emojis=emoji))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)