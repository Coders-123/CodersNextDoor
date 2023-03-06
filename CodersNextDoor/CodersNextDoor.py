import pyrebase 
from flask import *
app = Flask(__name__)

config = {
     "apiKey": "AIzaSyBqzSqlvRFRnmD8QiTC4vpY82DzB7T2G4E",
     "authDomain": "tutordbauthenticate.firebaseapp.com",
     "databaseURL": "https://tutordbauthenticate-default-rtdb.firebaseio.com",
     "projectId": "tutordbauthenticate",
     "storageBucket": "tutordbauthenticate.appspot.com",
     "messagingSenderId": "928677714123",
     "measurementId": "G-0YRYZYELPH"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])

def basic(): 
    unsuccessful = 'Please Check Your Email Or Password'
    successful = 'Login Successful'
    if request.method == 'POST': 
        email = request.form['name']
        password = request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('Login.html', s=successful)
        except:
            return render_template('Login.html', us=unsuccessful)
        
    return render_template('Login.html')

if __name__ == '__main__':
    app.run()

