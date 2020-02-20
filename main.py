from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage
)
import os
import random

app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    message = judge(hands_to_int(event.message.text), select_bothand())
    line_bot_api.reply_message(
        event.reply_token,
        message
    )

def select_bothand():
    return random.randint(0, 2)

def hands_to_int(userhand):
	if userhand == "グー":
		return 0
	if userhand == "チョキ":
		return 1
	if userhand == "パー":
		return 2
 

def judge(userhand, bothand):
    #0:あいこ　1:botの勝ち　2:userの勝ち
    status = (userhand - bothand + 3) % 3

    if status == 0:
        message = TextSendMessage(text="あいこだよーん")
    elif status == 1: # 負け
        message = AudioSendMessage(
            original_content_url="https://linebot20200220.herokuapp.com/static/audios/stupid5.mp3",
            duration=2000
        )
    elif status == 2:
        message = ImageSendMessage(
            original_content_url = "https://linebot20200220.herokuapp.com/static/images/maxresdefault.jpg", 
            previewImageUrl = "https://linebot20200220.herokuapp.com/static/images/maxresdefault.jpg"
        )

            # 画像置くのが、めんどくさい人向け
            # https://dol.ismcdn.jp/mwimgs/c/8/670m/img_c8dad835c4b9134b067cc8b8efcab22f143142.jpg
            # をoriginal_content_urlとpreviewImageUrlにぶち込んでください

    return message


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
