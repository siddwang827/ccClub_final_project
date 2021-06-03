import requests
import json
from linebot import LineBotApi, WebhookHandler

headers = {"Authorization":"Bearer MNSSthpXrqXLuyyC7Kd44XealdPdmhitULX8CJcl4teyLKHU4lh4ohoA84VgfSbjN0tI7DPlR/JfUdwyKFoYCboWzE6WQiXYvn5nrx2QokTC+hBLcYaiOPP6c1Ddzwz0SNL9oijLuvyF4kfCTyeblwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

# body = {
#     "size": {"width": 2500, "height": 1686},
#     "selected": "true",
#     "name": "Controller",
#     "chatBarText": "Tap to open",
#     "areas":[
#         {
#           "bounds": {"x": 0, "y": 0, "width": 1250, "height": 843},
#           "action": {"type": "uri", "uri": "https://8a86c95c15c0.ngrok.io/rich_menu_1"},

#           "bounds": {"x": 1250, "y": 0, "width": 1250, "height": 843},
#           "action": {"type": "uri", "uri": "https://tw.news.yahoo.com/"},

#           "bounds": {"x": 0, "y": 843, "width": 1250, "height": 843},
#           "action": {"type": "uri", "uri": "https://movies.yahoo.com.tw/"},

#           "bounds": {"x": 1250, "y": 843, "width": 1250, "height": 843},
#           "action": {"type": "uri", "uri": "https://www.pttweb.cc/"},

#         }
#     ]
#   }

# # 註冊rich_menu_id, 每個linebot最多註冊1000個
# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
#                        headers=headers,data=json.dumps(body).encode('utf-8'))
# print(req.text)



# 刪除rich_menu_ID
body = {"richMenuId":"richmenu-4057744b4d5a2d88e1a1ad2d8811a428"}
req = requests.request('Delete', 'https://api.line.me/v2/bot/richmenu/richmenu-4057744b4d5a2d88e1a1ad2d8811a428', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))
print(req.text)


# #設定預設的rich_menu_ID
# req = requests.request('Post', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-4057744b4d5a2d88e1a1ad2d8811a428', headers=headers)
# print(req.text)

# 查看所有rich_menu_ID
# line_bot_api = LineBotApi('MNSSthpXrqXLuyyC7Kd44XealdPdmhitULX8CJcl4teyLKHU4lh4ohoA84VgfSbjN0tI7DPlR/JfUdwyKFoYCboWzE6WQiXYvn5nrx2QokTC+hBLcYaiOPP6c1Ddzwz0SNL9oijLuvyF4kfCTyeblwdB04t89/1O/w1cDnyilFU=')
# rich_menu_list = line_bot_api.get_rich_menu_list()
# for rich_menu in rich_menu_list:
#     print(rich_menu.rich_menu_id)


# # 新增圖片到rich meun id
# with open("C:\\Users\\sidd\\Desktop\\ccClub_final_project\\workoutholly\\rich_menu\\menutest123.jpg", 'rb') as f:
#     line_bot_api.set_rich_menu_image("richmenu-4057744b4d5a2d88e1a1ad2d8811a428", "image/jpeg", f)

# # 下載rich menu id 中的圖片
# content = line_bot_api.get_rich_menu_image('richmenu-92071d63b7a861fb9853887caad4c737')
# with open("C:\\Users\\sidd\\Desktop\\ccClub_final_project\\workoutholly\\rich_menu\\test4.jpg", 'wb') as fd:
#     for chunk in content.iter_content():
#         fd.write(chunk)

















# {"richMenuId":"richmenu-4057744b4d5a2d88e1a1ad2d8811a428"}