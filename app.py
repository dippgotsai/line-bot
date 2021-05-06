from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('i/8L5XcfiFAJ51b+Fx7SKIMyAzXFJ+a8bMu1T85rxKwwo2j0p0wnVWQbdEY6mhvTSNecrfiWVUG6lKUpzWJpEMCONM+9Yv1MW5J6PjiqSOhoY6Xd9yEgVgf5vCES8T0Mtmq25NW08I51Hj9PR1wSbgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2cfc18973148f1438a6025531056cfb3')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()