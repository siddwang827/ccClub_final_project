import sys
import requests
from workoutholly import app, db
from workoutholly.model import Web_format, Users, Positions, Exercises, Routines, RoutineAction
from flask import Flask, request, abort, render_template, jsonify, redirect, url_for, session
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, PostbackEvent
import json


sys.path.append('.')

import config

linebot_client = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)




# 計時器路由
@app.route('/timer/exercise=<exercise>&sets=<sets>&rest=<rest>', methods=['GET','POST'])
def get(exercise, sets, rest):

    data = {'exercise': exercise , 'sets': sets, 'rest': rest}

    return render_template('ak1.html', data=data)


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
    user_name = formData.pop('line_name')
    position = formData.pop('position')

    # 檢查課表中是否有重複填寫的動作選項
    try:
        check_exercises = [ list(formData.values())[i] for i in range(len(formData)) if i % 5 == 0 ]
        check_exercises_dict = dict()

        if len(check_exercises) != len(set(check_exercises)):

            return f"<h1>嗯...   (￣ ￣|||)</h1><h1>課表內有重複的動作！？請{user_name}回上一頁重新確認！</h1>"

        elif len(check_exercises) == 0:

            return f"<h1>嗯... </h1><h1>請在課表內至少安排一個動作！{user_name}該不會是想偷懶吧？ ಠ_ಠ</h1><h1>請回上一頁重新確認</h1>"

        for num in range(1, (len(check_exercises) + 1)):
            check_exercises_dict[formData[f'exercise_{num}']] = [
                formData[f'weight_{num}'], 
                formData[f'sets_{num}'], 
                formData[f'reps_{num}'], 
                formData[f'rest_{num}']
            ]

        submit_data_to_db(accessToken, position, check_exercises, check_exercises_dict)
        return f'<h1>成功上傳課表，{user_name} 隨時可以開始訓練啦！ ୧(๑•̀ㅁ•́๑)૭✧</h1>'
                    

    except KeyError:

        return f"<h1>嗯....    (￣ ￣|||)</h1><h1>有些動作規劃得不完整，請{user_name}回上一頁重新確認！ </h1>"

  
def submit_data_to_db(accessToken, position, check_exercises, check_exercises_dict):

    # 將表單中回傳的line access token 發出 request 到 line platform，並取回 user profile
    user_profile = requests.request('GET', f'https://api.line.me/v2/profile', headers={'Authorization':f'Bearer {accessToken}'})
    profile = json.loads(user_profile.text)
    lineuserid = profile['userId']

    user_db = Users.query.filter_by(lineuserid=lineuserid).first()
    position_db = Positions.query.filter_by(name=position).first()

    try:
        #將此user之前的課表先刪除，若user不存在userdata.id=none, 即報錯進入except 
        Routines.query.filter_by(user_id=user_db.id).filter_by(position_id=position_db.id).delete() 
        db.session.commit()

    # 上方報錯表示db內查詢不到lineuserid, 先新增user資料
    except: 
        user = Users(lineuserid)
        db.session.add(user)
        db.session.commit()
        user_db = Users.query.filter_by(lineuserid=lineuserid).first()
    
    finally:

        action = RoutineAction()
        action.add_routines_to_db(check_exercises, check_exercises_dict, user_db, position_db)

        
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
        return (f"哎呀!   ∑(O_O;)\n尚未設定【{position_name}肌群】的課表!?\n事不宜遲快進行課表規劃功能!")

    head = f"您目前【{position_name}肌群】訓練課表"
    routine_list = routine_table.to_dict(orient='records')
    output = ""
    for num in range(len(routine_list)):
        for i in range(len(routine_list[num])):
            output += f"{list(routine_list[num].keys())[i]} : {list(routine_list[num].values())[i]}"
        if num != len(routine_list)-1:
            output += "\n"

    if len(routine_list) == 1:

        end = "窩靠!?   ಠ▃ಠ\n就只排一個動作!?你就這?"

        return json.dumps({"head": head, "output": output, "end":end})

    return json.dumps({"head": head, "output": output})




# 開始健身路由
@app.route('/workout', methods=['GET', 'POST'])
def creat_temp_routine():

    formData = request.form.to_dict()
    position_name = formData['position']
    lineuserid = formData['user_id']

    action = RoutineAction()
    temp_routine_table = action.create_temp_routines(position_name, lineuserid)

    trans = Web_format(position_name)
    position_cn = trans.position_translate()

    if not temp_routine_table:
        return (f'哎呀!   ∑(O_O;)\n尚未設定【{position_cn}肌群】課表!?\n事不宜遲快進行課表規劃功能!')
    
    response = temp_routine_hint(position_name, lineuserid, position_cn)

    return response

def temp_routine_hint(position_name, lineuserid, position_cn):

    action = RoutineAction()
    routine_hint = action.get_routine_hint(position_name, lineuserid)

    routine = routine_hint[0].to_dict(orient='records')[0]
    
    last_exercise = routine_hint[1]
    sets = 0
    rest = 0
    exercise_name = ""

    head = f"開始進行【{position_cn}肌群】訓練"
    output= ""
    end = ""

    for key, value in routine.items():
        output += f"{key} : {value}\n"
        if key == '訓練動作':
            exercise_name = value      
        elif key == '訓練組數':
            sets = value
        elif key == '組間休息時間(sec)':
            rest = value

    output += f"\n點擊連結可以開啟輔助計時頁面\nhttps://f99c6c53e900.ngrok.io/timer/exercise={exercise_name}&sets={sets}&rest={rest}"

    if last_exercise:
    
        end = f"竟然真的只排一個動作!\n太偷懶了吧廢物!!! ಠ▃ಠ"
        return json.dumps({"head": head, "output": output, "end": end})

    return json.dumps({"head": head, "output": output})

@app.route('/next_exercise', methods=['GET', 'POST'])
def next_exercise_hint():

    formData = request.form.to_dict()
    lineuserid = formData['user_id']
    action = RoutineAction()
    next_exercise_hint = action.next_exercise_hint(lineuserid)

    if not next_exercise_hint:
        return f'您目前並未進行任何訓練唷'

    position_name = next_exercise_hint[1]
    trans = Web_format(position_name)
    position_cn = trans.position_translate()

    last_exercise = next_exercise_hint[2]
    routine = next_exercise_hint[0].to_dict(orient='records')[0]   
    sets = 0
    rest = 0
    exercise_name = ""

    head = f"正在進行【{position_cn}肌群】訓練\n下一個訓練動作是"
    output = ""
    end = ""
    for key, value in routine.items():
        output += f"{key} : {value}\n"
        if key == '訓練動作':
            exercise_name = value      
        elif key == '訓練組數':
            sets = value
        elif key == '組間休息時間(sec)':
            rest = value

    output += f"\n點擊下方連結可以開啟輔助計時頁面\nhttps://f99c6c53e900.ngrok.io/timer/exercise={exercise_name}&sets={sets}&rest={rest}"
    
    if last_exercise:

        end = f"本次【{position_cn}肌群】訓練已完成\n運動後請記得補充蛋白質才會越來越巨唷~"
    
        return json.dumps({"head": head, "output": output, "end": end})
    
    return json.dumps({"head": head, "output": output})



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
    profile = linebot_client.get_profile(event.source.user_id)
    username = profile.display_name
    
    if mtext == '課表規劃': 
        
        head = f'Hi {username}~\n請選擇一個部位進行課表規劃~'
        flexmessage = json.load(open('workoutholly/static/fm_create_routine.json','r',encoding='utf-8'))
        linebot_client.reply_message(event.reply_token, [TextMessage(text=head), FlexSendMessage('課表規劃', flexmessage)])

    
    elif mtext == '課表查詢':

        head = f'Hi {username}~\n想查詢哪個部位的訓練課表呢~'
        flexmessage = json.load(open('workoutholly/static/fm_search_routine.json','r',encoding='utf-8'))
        linebot_client.reply_message(event.reply_token, [TextMessage(text=head), FlexSendMessage('課表規劃', flexmessage)])


    elif mtext == '開始健身':

        head = f'Hi {username}~\n馬上選擇要訓練的部位吧!!'
        flexmessage = json.load(open('workoutholly/static/fm_workout.json','r',encoding='utf-8'))
        linebot_client.reply_message(event.reply_token, [TextMessage(text=head), FlexSendMessage('課表規劃', flexmessage)])


    elif mtext == '下個動作':

        user_id = event.source.user_id
        data = { 'user_id': user_id }
        head = f'Hi {username}~\n'
        searchRoutine = requests.request('POST', 'https://f99c6c53e900.ngrok.io//next_exercise', data=data)
        

        try:
            routine_hint = json.loads(searchRoutine.text)
            output = routine_hint['output']
            if 'end' in routine_hint:
                end = routine_hint['end']
                head = routine_hint['head']
                linebot_client.reply_message(event.reply_token, [TextMessage(text=head), TextMessage(text=output), TextMessage(text=end)])
            else:
                head = routine_hint['head'] 
                linebot_client.reply_message(event.reply_token, [TextMessage(text=head), TextMessage(text=output)])
        except:
            routine_hint = searchRoutine.text
            routine_hint = head + routine_hint
            linebot_client.reply_message(event.reply_token, [TextMessage(text=routine_hint)])

    elif mtext in ['幹', '操你媽', '機掰', '操', '幹你娘']:

        text1 = '罵髒話是不對的~\n'
        text2 = '罵髒話是不好的~\n'
        text3 = '那沒什麼事我先走了~'
        linebot_client.reply_message(event.reply_token, [TextMessage(text=text1), TextMessage(text=text2), TextMessage(text=text3)])


    else:
        
        user_id = event.source.user_id
        data = { 'user_id': user_id }
        head = f'不是吧!?{username}\n你不知道WorkoutHolly只需要點選圖文介面，就可使用所有功能嗎~'
        linebot_client.reply_message(event.reply_token, TextMessage(text=head))



@handler.add(PostbackEvent) 
def handle_postback(event):

    pd, user_id,= event.postback.data, event.source.user_id
    option = pd[:4]
    data = { 'user_id': user_id, 'position': pd[4:] }
    profile = linebot_client.get_profile(event.source.user_id)
    username = profile.display_name
    head = f"Hi {username}~\n"

    if option == '課表查詢':

        searchRoutine = requests.request('POST', 'https://f99c6c53e900.ngrok.io//routine_search', data=data)
        try:
            routine_query = json.loads(searchRoutine.text)
            print(routine_query)
            head += routine_query['head']
            output = routine_query['output']
            if 'end' in routine_query:
                end = routine_query['end']
                linebot_client.reply_message(event.reply_token, [TextMessage(text=head), TextMessage(text=output), TextMessage(text=end)])
            else:
                linebot_client.reply_message(event.reply_token, [TextMessage(text=head), TextMessage(text=output)])
        except:
            output = searchRoutine.text
            linebot_client.reply_message(event.reply_token, TextMessage(text=output))


    elif option == '開始健身':

        searchRoutine = requests.request('POST', 'https://f99c6c53e900.ngrok.io//workout', data=data)
        try:
            routine_hint = json.loads(searchRoutine.text)
            head += routine_hint['head']
            output = routine_hint['output']
            if 'end' in routine_hint:
                end = routine_hint['end']
                linebot_client.reply_message(event.reply_token, [TextMessage(text=head), TextMessage(text=output), TextMessage(text=end)])
            else:
                linebot_client.reply_message(event.reply_token, [TextMessage(text=head), TextMessage(text=output)])
        except:
            routine_hint = searchRoutine.text
            linebot_client.reply_message(event.reply_token, [TextMessage(text=routine_hint)])

    
    


