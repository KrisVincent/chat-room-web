from datetime import timedelta
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "y@m3T32"
<<<<<<< HEAD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_app.sqlite3'
=======
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://kqdnjldtzrsfhr:d29c453745d28478d088ba4487ce4e095ab61fd3be1a89ff04eb020db3cb8ca0@ec2-34-230-198-12.compute-1.amazonaws.com:5432/dckninmla9hluj"
>>>>>>> 29e4ddb039086b35d8f4b2b770239cf1072d5fbb
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=15)
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


class messages(db.Model):

    message_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer)
    message_content = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    date = db.Column(db.DateTime())

    def __init__(self, client_id, message_content,nickname,date):
        self.client_id = client_id
        self.message_content = message_content 
        self.nickname = nickname
        self.date = date
        
