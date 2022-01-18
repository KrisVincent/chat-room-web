import io
from logging import info
from flask import Flask, redirect, url_for, render_template,session, flash, request
import flask
from sqlalchemy import *
from flask.helpers import flash
from flask_socketio import SocketIO, send
frtoom database import account,messages, db,app
from datetime import datetime
import PIL.Image as Image



socketio = SocketIO( app )

#this function is the index of the web app which is login page
@app.route("/", methods = ["POST","GET"])
def login_page():

    if "username" in session:

        return redirect(url_for("chat_page"))



    #if user presses login button
    if request.method == "POST":
        
        #get the required login data
        get_username = request.form["username"]
        get_password = request.form["password"]

        #check if username exists and password entered is correct
        user_exists = check_login(get_username,get_password)

        #this just checks if user exists or not
        if user_exists:
            

            flash(f"login successfully! welcome {get_username}","info")
            session["nickname"] = user_exists.client_nickname
            session["username"] = user_exists.client_username
           
            return redirect(url_for("chat_page"))

        else:

            flash("Wrong password or username does not exists!", "info")

            return redirect(url_for("login_page"))


    return render_template("login_page.html")

#this function is responsible for the registration page
@app.route("/register", methods = ["POST","GET"])
def register_page():

    if request.method == "POST":
        try:
           
            #to get the image file then input to database
            get_file = request.files['image']
            image = Image.open(get_file)
            
            byteIO = io.BytesIO()
            image.save(byteIO, format='PNG', quality=95)
            get_file = byteIO.getvalue() # this is the output

            #get all the required data for registration
            get_username = request.form["username"]
            get_password = request.form["password"]
            get_confirm_password = request.form["confirm_password"]
            get_nickname = request.form["nickname"]
            get_email = request.form["email"]
            get_gender = request.form["gender"]
            
         
           
        #some exceptions especially for file uploads
        except Exception as err:
            print("Error occurred")
            print(err)
            flash(f" Please Remember to actually choose something :D", "info")

        #this is to check if confirm and password are the same if not inform and redirect
        if get_password != get_confirm_password:

            flash(f"Make sure your password and cofirm password are the same!", "info")

            return redirect(url_for("register_page"))

        user_exists = insert_account_data(get_username,
                                         get_password,
                                         get_nickname,
                                         get_email,
                                         get_gender,
                                         get_file)
        
        #inform the user that username already existing
        if user_exists:
            flash(f"The username {get_username} or email {get_email} already registered", "info")

            return redirect(url_for("register_page"))

        flash("Registration succesful!", "info")
        return redirect(url_for("login_page"))



      

    return render_template("register_page.html")


@app.route( '/chat-room', methods = ["POST","GET"] )
def chat_page():

    #this will get all the message from the database
    message_list = messages.query.order_by(messages.message_id)

    
    print(message_list)
    #redirect if user is not in session
    if "nickname" not in session:
        return redirect(url_for("login_page"))
  
    
    return render_template( 'chat_room.html' ,msg = message_list)



@socketio.on( 'handle_msgs' )
def handle_my_custom_event( json ):

  #get client_id for message data insertion
  client_id = get_client_id(session["username"])
  now = datetime.now()
 


  # dd/mm/YY H:M:S
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  
  #this is used to get client's data
  user = account.query.filter_by(client_id = client_id).first()


  #store data in a dictionary
  msg_data = {
  "nickname": user.client_nickname,
  "image": user.client_image,
  "message": json["message"],
  "date" : dt_string
   }   
 

  #insert message data
  message_data(client_id,json["message"],session["nickname"])
  
  #this is for the live data and pass the msg_data dictionary
  socketio.emit( 'live_chat', msg_data)






#the following code below are the all database functions

def message_data(client_id,message,nickname):
    
    now = datetime.now()
   
    user = messages(
                    client_id,
                    message,
                    nickname,
                    now
    )
   
    db.session.add(user)

    db.session.commit()


def get_client_id(username):
    user_exists = account.query.filter_by(client_username = username).first()

    if user_exists:
        return user_exists.client_id
    else:
        return False

#This function is responsible for inserting registration data into the database
def insert_account_data(username,password,nickname,email,gender,image):
    
    #store our data
    user = account(username,
                   password,
                   nickname,
                   email,
                   gender,
                   image)


    #check if username already exists via using our username to check
    user_exists = account.query.filter_by(client_username = username).first()
   
   
    #this is for email same function as user_exists but with email 
    #this will be used for password recovery later on
    email_exists = account.query.filter_by(client_email = email).first()
    #simply return True if user already exists



    if user_exists or email_exists:

        return True

    else:
        db.session.add(user)

        db.session.commit()

        return False

#this checks if the user login data matches with any of our data in database
def check_login(username, password):

    #this part checks whether or not username being registered exists  
    user_exists = account.query.filter_by(client_username = username).first()

    if user_exists:

        get_user_password = user_exists.client_password

        if get_user_password == password:

            return user_exists


    return False

if __name__ == "__main__":
    
    socketio.run( app, debug = True )
    db.create_all() # create database model
    
     