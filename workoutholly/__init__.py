
from flask import Flask #載入 Flask
from flask_sqlalchemy import SQLAlchemy



import config




app = Flask(__name__) #建立 Application物件



# 配置資料庫連線
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

