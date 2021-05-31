from workoutholly import app
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import config

linebot_client = LineBotApi(config.LINE_CHANNEL_SECRET)
linebot_handler = WebhookHandler(config.LINE_CHANNEL_ACCESS_TOKEN)


@app.route('/')
def index():
    
    return "<h1>Hello World</h1>"




# 當人有呼叫 https://your-app-name.herokuapp.com/callback 時，會call這隻函數
# 這支函數是當 Message API 將資料送過來時，必須先做的處理(認證是否有效)
@app.route('/callback', methods=['POST'])
def callback():
    # 取得http header中的X-Line-Signature項目，該項目的內容值是即為數位簽章
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    try:
        linebot_handler.handle(body, signature)   

    except InvalidSignatureError: # 數位簽章錯誤
        abort(400)

    return 'ok'



@handler.add(MessageEvent, message=TextMessage)


   

