# ## flex message 模板



# # TemplateSendMessage - ConfirmTemplate
# confirm_template_message = TemplateSendMessage(
#     alt_text='Confirm template',
#     template=ConfirmTemplate(
#         text='Are you sure?',
#         actions=[
#             PostbackAction(
#                 label='postback',
#                 display_text='postback text',
#                 data='action=buy&itemid=1'
#             ),
#             MessageAction(
#                 label='message',
#                 text='message text'
#             )
#         ]
#     )
# )


# # TemplateSendMessage - ButtonsTemplate
# buttons_template_message = TemplateSendMessage(
#     alt_text='Buttons template',
#     template=ButtonsTemplate(
#         thumbnail_image_url='https://example.com/image.jpg',
#         title='Menu',
#         text='Please select',
#         actions=[
#             PostbackAction(
#                 label='postback',
#                 display_text='postback text',
#                 data='action=buy&itemid=1'
#             ),
#             MessageAction(
#                 label='message',
#                 text='message text'
#             ),
#             URIAction(
#                 label='uri',
#                 uri='http://example.com/'
#             )
#         ]
#     )
# )

single_weight = [ n * 2.5 if n < 12 else (n-6) * 5 for n in range(1, 27) ]
print(single_weight)
