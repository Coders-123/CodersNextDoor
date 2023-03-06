import pyrebase 
from flask import *
app = Flask(__name__)

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'codersnextdoor1.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "username@gmail.com"
app.config['MAIL_PASSWORD'] = "password"
mail = Mail(app)

msg = Message()
msg.subject = "Email Subject"
msg.recipients = ['recipient@gmail.com']
msg.sender = 'username@gmail.com'
msg.body = 'Email body'
mail.send(msg)

from threading import Thread

def send_email(app, msg):
    with app.app_context():
        mail.send(msg)
msg = Message()
msg.subject = "Email Subject"
msg.recipients = ['recipient@gmail.com']
msg.sender = 'username@gmail.com'
msg.body = 'Email body'
Thread(target=send_email, args=(app, msg)).start()

models.py
...
    def get_reset_token(self, expires=500):
        return jwt.encode({'reset_password': self.username,
                           'exp':    time() + expires},
                           key=os.getenv('SECRET_KEY_FLASK'))
email.py
...
def send_email(user):
    token = user.get_reset_token()
    msg = Message()
    msg.subject = "Flask App Password Reset"
    msg.sender = os.getenv('MAIL_USERNAME')
    msg.recipients = [user.email]
    msg.html = render_template('reset_email.html',
                                user=user, 
                                token=token)
mail.send(msg)

def verify_reset_token(token):
        try:
            username = jwt.decode(token,
              key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
        except Exception as e:
            print(e)
            return
        return User.query.filter_by(username=username).first()