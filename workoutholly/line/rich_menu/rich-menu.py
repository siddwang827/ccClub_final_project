import requests
import json
from linebot import LineBotApi, WebhookHandler

headers = {"Authorization":"Bearer <LINE_CHANNEL_ACCESS_TOKEN>"}

# body = {
#     "size": {"width": 2500, "height": 1686},
#     "selected": "true",
#     "name": "Controller",
#     "chatBarText": "Tap to open",
#     "areas":[
#         {
#           "bounds": {"x": 0, "y": 0, "width": 1250, "height": 843},
#           "action": {"type": "uri", "uri": "https://tw.stock.yahoo.com/"},

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
body = {"richMenuId":"<rich_menu_id>"}
req = requests.request('Delete', 'https://api.line.me/v2/bot/richmenu/<rich_menu_id>', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))
print(req.text)


# #設定預設的rich_menu_ID
# req = requests.request('Post', 'https://api.line.me/v2/bot/user/all/richmenu/<rich_menu_id>', headers=headers)
# print(req.text)

# 查看所有rich_menu_ID
# line_bot_api = LineBotApi('<LINE_CHANNEL_ACCESS_TOKEN>')
# rich_menu_list = line_bot_api.get_rich_menu_list()
# for rich_menu in rich_menu_list:
#     print(rich_menu.rich_menu_id)


# # 新增圖片到rich meun id
# with open("image_path", 'rb') as f:
#     line_bot_api.set_rich_menu_image("<rich_menu_id>", "image/jpeg", f)

# # 下載rich menu id 中的圖片
# content = line_bot_api.get_rich_menu_image('<rich_menu_id>')
# with open("<image_path>", 'wb') as fd:
#     for chunk in content.iter_content():
#         fd.write(chunk)

















# {"richMenuId":"richmenu-4057744b4d5a2d88e1a1ad2d8811a428"}