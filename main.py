import io
from logging import info
from flask import Flask, redirect, url_for, render_template,session, flash, request
import flask
from flask.helpers import flash
from database import account, db,app
import PIL.Image as Image


#this function is the index of the web app which is login page
@app.route("/", methods = ["POST","GET"])
def login_page():

    #if user presses login button
    if request.method == "POST":
        
        #get the required login data
        get_username = request.form["username"]
        get_password = request.form["password"]

        #check if username exists and password entered is correct
        user_exists = check_login(get_username,get_password)

        if user_exists:
            

            flash(f"login successfully! welcome {get_username}","info")

            return redirect(url_for("login_page"))

        else:

            flash("Wrong password or username does not exists!", "info")

            return redirect(url_for("login_page"))


    return render_template("login_page.html")

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

#This function is responsible for inserting registration data into the data base
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


    user_exists = account.query.filter_by(client_username = username).first()

    if user_exists:

        get_user_password = user_exists.client_password

        if get_user_password == password:

            return user_exists


    return False

if __name__ == "__main__":
     app.run(debug=True) # for bugs and testing purposes
     db.create_all() # create database model
     