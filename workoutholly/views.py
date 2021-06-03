from linebot.models.events import PostbackEvent
from workoutholly import app
from workoutholly.model import web_table
from flask import Flask, request, abort, render_template, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent, FlexSendMessage
import json

import config

linebot_client = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)





@app.route('/',methods=['GET', 'POST'])
def index():
    text = {'arg1':'1', 'arg2': '2'}

    return render_template('timer.html', data=text)



@app.route('/create_routine/<position>', methods=['POST', 'GET'])
def create_routine(position):

    table = web_table(position)
    th = table.tabel_head
    weight = table.weight_select
    sets = table.sets_select 
    reps = table.reps_select
    rest = table.rest_select
    exercises = table.choose_exercises(position)
    return render_template('routine_set copy.html', th=th, exercises=exercises, position=position, weight=weight, sets=sets, reps=reps, rest=rest)


@app.route('/routinesubmit', methods=[ 'POST'])
def post_form():
    data =  json.dumps(request.form)
    data_j = json.loads(data)
    

    print(type(data))
    print(data)
    print(type(data_j))
    print(data_j)

    return data



# 當人有呼叫 https://your-app-name.herokuapp.com/callback 時，會call這隻函數
# 這支函數是當 Message API 將資料送過來時，必須先做的處理(認證是否有效)
@app.route('/callback', methods=['POST'])
def callback():
    # 取得http header中的X-Line-Signature項目，該項目的內容值是即為數位簽章
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)   

    except InvalidSignatureError: # 數位簽章錯誤
        abort(400)

    return 'ok'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_text_message(event):

#     # 當 LINE 後台發送測試訊號過來時，會使用一組假 token，無視它就好
#     if event.reply_token == '0' * 32:
#         return 

#     # 暫停 1.5 秒，假裝在打字或讀訊息


#     # 隨機回覆一串敷衍訊息
#     linebot_client.reply_message(
#         event.reply_token,
#         TextSendMessage(
#             'https://8a86c95c15c0.ngrok.io/rich_menu_1')
#         )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    
    if mtext == '課表規劃':
        FlexMessage = json.load(open('C:\\Users\\sidd\\Desktop\\ccClub_final_project\\workoutholly\\static\\flexMessage.json','r',encoding='utf-8'))
        linebot_client.reply_message(event.reply_token, FlexSendMessage('課表規劃',FlexMessage))



# @app.route('/rich_menu_1', methods=['POST', 'GET'])
# @handler.add(PostbackEvent)
# def handle_post_event(event):
#     postBack = event.postback.data
#     print(type(postBack))
#     position = postBack[2] # 從postback回的content中撈取部位關鍵字
#     table = web_table(position)
#     exercises = table.choose_exercises(position)
#     th = table.tabel_head
#     weight = table.weight_select
#     sets = table.sets_select 
#     reps = table.reps_select
#     rest = table.rest_select

#     if postBack[:2] == '規劃':



#         # linebot_client.reply_message(event.reply_token, TextSendMessage('https://2acfebd2364b.ngrok.io//rich_menu_1'))

#         return render_template('routine_set copy.html', th=th, exercises=exercises, position=position, 
#                                 weight=weight, sets=sets, reps=reps, rest=rest)


    
    


