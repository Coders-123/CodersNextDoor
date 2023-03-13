import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

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

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

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
           
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
           
            return redirect(url_for('welcome'))
        except:
           
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run(debug=True)