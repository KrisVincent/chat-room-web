from datetime import timedelta
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "y@m3T32"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_app.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)

class account(db.Model):

    client_id = db.Column(db.Integer, primary_key=True)
    client_username = db.Column(db.String(100))
    client_password = db.Column(db.String(100))
    client_nickname = db.Column(db.String(100))
    client_email  = db.Column(db.String(100))
    client_gender  = db.Column(db.String(100))
    client_image = db.Column(db.LargeBinary)


    def __init__(self, username,password,nickname,email,gender,image):
        self.client_username = username
        self.client_password = password
        self.client_nickname = nickname
        self.client_email = email
        self.client_gender = gender
        self.client_image = image   

