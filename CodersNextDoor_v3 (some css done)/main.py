import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from firebase_admin import credentials, firestore
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials, firestore
from firebase_admin import auth
from flask_session import Session
from firebase_admin import auth





app=Flask(__name__)

config = {
  "apiKey": "AIzaSyBqzSqlvRFRnmD8QiTC4vpY82DzB7T2G4E",
  "authDomain": "tutordbauthenticate.firebaseapp.com",
  "databaseURL": "https://tutordbauthenticate-default-rtdb.firebaseio.com",
  "projectId": "tutordbauthenticate",
  "storageBucket": "tutordbauthenticate.appspot.com",
  "messagingSenderId": "928677714123",
  "appId": "1:928677714123:web:a7aebab830141d57a8234e",
  "measurementId": "G-0YRYZYELPH"
}



firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}
#login route
@app.route("/")
def login():
 
 if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Sign in the user
            user = auth.sign_in_with_email_and_password(email, password)

            # Check if the user's email has been verified
            if user['emailVerified']:
                session['user'] = user['idToken']
                flash('Logged in successfully.', 'success')
                return redirect(url_for('home'))
            else:
                flash('Please verify your email before logging in.', 'error')
                return redirect(url_for('login'))
        except:
            flash('Login failed. Please check your credentials and try again.', 'error')
            return redirect(url_for('login'))

   
 return render_template("login.html")
   
#signup route
@app.route("/signup")
def signup():
    return render_template("signup.html")

#welcome route
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
       
       
        return render_template("welcome.html", email = person["email"], name = person["name"])
       
    else:
        return redirect(url_for('login'))

#result for signing in 
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        
        result = request.form           
        email = result["email"]
        password = result["pass"]
        try:
            
            user = auth.sign_in_with_email_and_password(email, password)
            
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            
            return redirect(url_for('welcome'))
        except:
           
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#result for register for signup
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        
        result = request.form           
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            
            auth.create_user_with_email_and_password(email, password)
           
            user = auth.sign_in_with_email_and_password(email, password)

            auth.send_email_verification(user['idToken'])
            flash('Verification email sent. Please check your inbox.', 'success')
            return redirect(url_for('login'))
           
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
           
            return redirect(url_for('welcome'))
        except:
            flash('Registration failed. Please try again.', 'error')           
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))
        

@app.route("/applicationconfirm")
def applicationconfirm():
    return render_template("applicationconfirm.html")



@app.route("/application", methods = ["POST", "GET"]) 
def applicationpage():
    if request.method == "POST":
        
        
        #passing of data
        studemail = request.form["DUTemail"]  
        studfname= request.form["fname"]
        studlname=request.form["lname"]
        studNo= request.form["Snum"]
        studIDno=request.form["IDnum"]
        studcontact=request.form["Contact"]
        
        #banking details
        #studtaxno=request.form["tax_number"]
        
        studbankname= request.form["bank_name"]
        
        #studfile= request.files["file"]
        
        studentapplication={"email":studemail,"First Name":studfname,"Last Name":studlname,"Student Number":studNo, "ID Number":studIDno, "Contact Number":studcontact}
       # StudentBankDetails={}
        
        
        db.child("Tutors").child(person["uid"]).set(studentapplication)
        disp=db.child("Tutors").get()
        
        print(disp.val())
     
        return redirect(url_for("applicationconfirm")) 
 
    else:
     return render_template("tutapplication.html")   
    

#for password reset

'''@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        try:
            auth.send_password_reset_email(email)
            flash("A password reset link has been sent to your email.", "success")
            return redirect(url_for("login"))
        except:
            flash("Failed to send password reset email. Please try again later.", "error")
            return redirect(url_for("forgot_password"))
    else:
        return render_template("forgot_password.html")'''
    
#password reset being used is coded below 
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        try:
            auth.send_password_reset_email(email)
            flash("A password reset link has been sent to your email.", "success")
            return redirect(url_for("login.html"))
        except Exception as e:
            flash("Failed to send password reset email. Please try again later.", "error")
            print(e)
            return redirect(url_for("forgot_password.html"))
    else:
        return render_template("forgot_password.html")
    

#HR Redirect for Login (not working)
@app.route('/')
def HR():
    # redirect to the "HR" route
    return redirect(url_for('HR_login.html'))

@app.route('/HR_login')
def HR_New():
    return render_template('HR_login.html')
    

if __name__ == "__main__":
    app.run() 
    
    
    
    
    
    ######### test to see if it writes to table with Tutor child 
 #      studentdata = {"Age": 24, "Name": "Fred", "Tutor": True}
        #to create data
  #      db.child("Tutors").child(person["uid"]).set(studentdata)