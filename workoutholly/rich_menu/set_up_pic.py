from linebot import LineBotApi, WebhookHandler


line_bot_api = LineBotApi('MNSSthpXrqXLuyyC7Kd44XealdPdmhitULX8CJcl4teyLKHU4lh4ohoA84VgfSbjN0tI7DPlR/JfUdwyKFoYCboWzE6WQiXYvn5nrx2QokTC+hBLcYaiOPP6c1Ddzwz0SNL9oijLuvyF4kfCTyeblwdB04t89/1O/w1cDnyilFU=')

with open("C:\\Users\\sidd\\Desktop\\ccClub_final_project\\workoutholly\\rich_menu\\menutest123.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-4057744b4d5a2d88e1a1ad2d8811a428", "image/jpeg", f)

# content = line_bot_api.get_rich_menu_image('richmenu-92071d63b7a861fb9853887caad4c737')
# with open("C:\\Users\\sidd\\Desktop\\ccClub_final_project\\workoutholly\\rich_menu\\test4.jpg", 'wb') as fd:
#     for chunk in content.iter_content():
#         fd.write(chunk)