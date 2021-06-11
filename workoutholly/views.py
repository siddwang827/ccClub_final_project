import sys
import requests
from workoutholly import app, db
from workoutholly.model import Web_format, Users, Positions, Exercises, Routines, RoutineAction
from flask import Flask, request, abort, render_template, jsonify, redirect, url_for, session
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, PostbackEvent
import json
import ast

sys.path.append('.')

import config

linebot_client = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)




# 計時器路由
@app.route('/timer/exercise=<exercise>&sets=<sets>&rest=<rest>', methods=['GET','POST'])
def get(exercise, sets, rest):

    data = {'exercise': exercise , 'sets': sets, 'rest': rest}

    return render_template('ak1.html', data=data)

    # session['data'] = data
    # return redirect(url_for('timer'), data=data)

# @app.route('/timer', methods=['POST'])
# def timer():

#     data = request.args['data']
#     data = data['messages']
    
#     return render_template('ak1.html', data=data.to_dict())


# 課表規劃網頁路由
@app.route('/create_routine/<position>', methods=['POST', 'GET'])
def create_routine(position):
    
    webFormat = Web_format(position)
    th = webFormat.tabel_head
    weight = webFormat.weight_select
    sets = webFormat.sets_select 
    reps = webFormat.reps_select
    rest = webFormat.rest_select
    exercises = webFormat.choose_exercises()
    return render_template('routine_set.html', th=th, exercises=exercises, position=position, weight=weight, sets=sets, reps=reps, rest=rest)


# 課表submit新增至資料庫路由
@app.route('/routine_submit', methods=['POST'])
def check_form():

    formData = request.form.to_dict()
    accessToken = formData.pop('access_token')
    position = formData.pop('position')
    # 檢查課表中是否有重複填寫的動作選項
    try:
        check_exercises = [ list(formData.values())[i] for i in range(len(formData)) if i % 5 == 0 ]
        check_exercises_dict = dict()

        if len(check_exercises) != len(set(check_exercises)):

            return "<h1>課表內有重複的動作唷，請巨巨重新確認！</h1>"

        elif len(check_exercises) == 0:

            return "<h1>請巨巨在課表內至少安排一個動作！該不會是想偷懶吧？ ಠ_ಠ</h1>"

        for num in range(1, (len(check_exercises) + 1)):
            check_exercises_dict[formData[f'exercise_{num}']] = [
                formData[f'weight_{num}'], 
                formData[f'sets_{num}'], 
                formData[f'reps_{num}'], 
                formData[f'rest_{num}']
            ]
        # print(check_exercises)
        # print(check_exercises_dict)
        submit_data_to_db(accessToken, position, check_exercises, check_exercises_dict)
        return "<h1>成功上傳課表，巨巨隨時可以開始訓練啦！ ୧(๑•̀ㅁ•́๑)૭✧</h1>"

    except KeyError:

        return "<h1>有些動作規劃得不完整，請巨巨重新確認！ (￣ ￣|||)</h1>"

  
def submit_data_to_db(accessToken, position, check_exercises, check_exercises_dict):

    # 將表單中回傳的line access token 發出 request 到 line platform，並取回 user profile
    user_profile = requests.request('GET', f'https://api.line.me/v2/profile', headers={'Authorization':f'Bearer {accessToken}'})
    profile = json.loads(user_profile.text)
    lineuserid = profile['userId']

    # 檢查此line userid 是否存在於database中
    user_db = Users.query.filter_by(lineuserid=lineuserid).first()
    position_db = Positions.query.filter_by(name=position).first()
    try:
        #將此user之前的課表先刪除，若user不存在userdata.id=none, 即報錯進入except 
        Routines.query.filter_by(user_id=user_db.id).filter_by(position_id=position_db.id).delete() 
        db.session.commit()
        print('成功')

    # 上方報錯表示db內查詢不到lineuserid, 先新增user資料
    except: 
        user = Users(lineuserid)
        db.session.add(user)
        db.session.commit()
        user_db = Users.query.filter_by(lineuserid=lineuserid).first()
    
    finally:

        action = RoutineAction()
        action.Add_routines_to_db(check_exercises, check_exercises_dict, user_db, position_db)

        
# 課表查詢路由
@app.route('/routine_search', methods=['GET', 'POST'])
def searh_routine():

    formData = request.form.to_dict()
    position_name = formData['position']
    lineuserid = formData['user_id']

    action = RoutineAction()
    routine_table = action.get_routine(position_name, lineuserid)

    trans = Web_format(position_name)
    position_name = trans.position_translate()
    

    if routine_table.empty:
        return (f'∑(O_O;)\n巨巨尚未設定【{position_name}肌群】的課表!?\n事不宜遲趕快先進行課表規劃功能!')

    output = f'{position_name}部肌群訓練課表\n'
    routine_list = routine_table.to_dict(orient='records')
    
    for ele in routine_list:
        output += f'\n'
        for i in range(len(ele)):
            output += f'{list(ele.keys())[i]} : {list(ele.values())[i]}\n'

    return output


# 開始健身路由
@app.route('/workout', methods=['GET', 'POST'])
def creat_temp_routine():

    formData = request.form.to_dict()
    position_name = formData['position']
    lineuserid = formData['user_id']
    action = RoutineAction()
    temp_routine_table = action.Create_temp_routines(position_name, lineuserid)

    trans = Web_format(position_name)
    position_cn = trans.position_translate()

    if not temp_routine_table:
        return (f'∑(O_O;)\n巨巨尚未設定【{position_cn}肌群】的課表!?\n事不宜遲趕快先進行課表規劃功能!')
    
    response = temp_routine_hint(position_name, lineuserid, position_cn)

    return response

def temp_routine_hint(position_name, lineuserid, position_cn):

    action = RoutineAction()
    routine_hint = action.get_routine_hint(position_name, lineuserid)
    print(routine_hint)

    routine = routine_hint.to_dict(orient='records')[0]
    
    sets = 0
    rest = 0
    exercise_name = str()

    output = f'巨巨現在進行的是【{position_cn}部肌群】訓練\n\n'

    for key, value in routine.items():
        output += f'{key} : {value}\n'
        if key == '訓練動作':
            exercise_name = value      
        elif key == '訓練組數':
            sets = value
        elif key == '組間休息時間(sec)':
            rest = value

    output += f'\n點擊下方連結可以開啟輔助計時頁面~\n\nhttps://f99c6c53e900.ngrok.io/timer/exercise={exercise_name}&sets={sets}&rest={rest}'

    return output

@app.route('/next_exercise', methods=['GET', 'POST'])
def next_exercise_hint():

    formData = request.form.to_dict()
    lineuserid = formData['user_id']
    action = RoutineAction()
    next_exercise_hint = action.next_exercise_hint(lineuserid)

    if not next_exercise_hint:
        return f'本次訓練動作已全部結束啦!\n運動後請記得補充蛋白質才會越來越巨唷~'

    position_name = next_exercise_hint[1]
    trans = Web_format(position_name)
    position_cn = trans.position_translate()

    

    routine = next_exercise_hint[0].to_dict(orient='records')[0]   
    sets = 0
    rest = 0
    exercise_name = str()

    output = f'巨巨現在進行的是【{position_cn}部肌群】訓練\n\n'

    for key, value in routine.items():
        output += f'{key} : {value}\n'
        if key == '訓練動作':
            exercise_name = value      
        elif key == '訓練組數':
            sets = value
        elif key == '組間休息時間(sec)':
            rest = value

    output += f'\n點擊下方連結可以開啟輔助計時頁面~\n\nhttps://f99c6c53e900.ngrok.io/timer/exercise={exercise_name}&sets={sets}&rest={rest}'

    return output



#linebot 路由設定
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

# 定義MessageEvent觸發時執行的動作
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    
    if mtext == '課表規劃':

        flexmessage = json.load(open('workoutholly/static/fm_create_routine.json','r',encoding='utf-8'))
        linebot_client.reply_message(event.reply_token, FlexSendMessage('課表規劃', flexmessage))
    
    elif mtext == '課表查詢':

        flexmessage = json.load(open('workoutholly/static/fm_search_routine.json','r',encoding='utf-8'))
        linebot_client.reply_message(event.reply_token, FlexSendMessage('課表查詢', flexmessage))

    elif mtext == '開始健身':

        flexmessage = json.load(open('workoutholly/static/fm_workout.json','r',encoding='utf-8'))
        linebot_client.reply_message(event.reply_token, FlexSendMessage('開始健身', flexmessage))

    elif mtext == '下個動作':

        user_id = event.source.user_id
        data = {'user_id': user_id}
        searchRoutine = requests.request('POST', 'https://f99c6c53e900.ngrok.io//next_exercise', data=data)
        routine_hint = searchRoutine.text
        linebot_client.reply_message(event.reply_token, TextMessage(text=routine_hint))

    # elif mtext == '下個動作':

        

        

        # 回傳選項給user (flex Message 設定action為text)
        # user點選查詢該部位課表 
        # user帶入回傳查詢該部位課表
        # MessageEvent 判定 "查詢X部課表"
        # 回傳圖片
        
@handler.add(PostbackEvent) 
def handle_postback(event):

    pd, user_id,= event.postback.data, event.source.user_id
    option = pd[:4]
    data = { 'user_id': user_id, 'position': pd[4:] }
    
    if option == '課表查詢':

        searchRoutine = requests.request('POST', 'https://f99c6c53e900.ngrok.io//routine_search', data=data)
        routine = searchRoutine.text
        linebot_client.reply_message(event.reply_token, TextMessage(text=routine))

    elif option == '開始健身':

        searchRoutine = requests.request('POST', 'https://f99c6c53e900.ngrok.io//workout', data=data)
        routine_hint = searchRoutine.text
        linebot_client.reply_message(event.reply_token, TextMessage(text=routine_hint))
    
    


