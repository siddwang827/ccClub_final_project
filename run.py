from workoutholly import app
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from workoutholly import views







if __name__ == '__main__':
    app.run( debug=True)



