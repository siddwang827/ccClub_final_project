
from workoutholly import app
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import config

linebot_client = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
linebot_handler = WebhookHandler(config.LINE_CHANNEL_SECRET)



# @app.route('/')
# def index():
        
#     return  'Hello flask'


@app.route('/')
def index():

    return render_template('chest.html')

@app.route('/chest', methods=[ 'POST'])
def post_form():
    fname = request.form.get('fname')
    lname = request.form.get('lname')

    print(fname, lname)

    return 'ok'





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

@linebot_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):

    # 當 LINE 後台發送測試訊號過來時，會使用一組假 token，無視它就好
    if event.reply_token == '0' * 32:
        return 

    # 暫停 1.5 秒，假裝在打字或讀訊息


    # 隨機回覆一串敷衍訊息
    linebot_client.reply_message(
        event.reply_token,
        TextSendMessage(
            '放妳嗎狗屁！')
        )
    




