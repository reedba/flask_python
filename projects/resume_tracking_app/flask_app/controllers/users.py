from flask_bcrypt import Bcrypt
from flask import render_template, flash, session, request, redirect
from flask_app import app
from flask_app.models.user_model import User
from flask_mail import Mail, Message

bcrypt = Bcrypt(app)
mail = Mail(app)


#Start of email authentication
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'brandon.andrew.reed@gmail.com'
app.config['MAIL_PASSWORD'] = ''
#app.config['MAIL_USE_TLS'] = 'False'
app.config['MAIL_USE_SSL'] = 'True'
mail = Mail(app)


#   Create a token for security purposes
#   add the token to the url link
#   Check if email matches in the Database
#   If email is in database then send message to email address provided
#   redirect to the update password page

@app.route('/send_message', methods=['POST'])
def send_email():
    msg = Message('Hello', sender='brandon.andrew.reed@gmail.com', recipients=['brandon.andrew.reed@gmail.com'])
    msg.body = "Yay it works!"
    mail.send(msg)
    return 'Sent'       



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/reset_email')
def reset_password():
    return render_template('reset_email.html')

@app.route('/update_pw_page')
def reset_page():
    return render_template('update_pw.html')

@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/login')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



