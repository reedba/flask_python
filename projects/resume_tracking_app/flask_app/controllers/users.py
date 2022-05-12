from flask_bcrypt import Bcrypt
from flask import render_template, flash, session, request, redirect, url_for
from flask_app import app
from flask_app.models.user_model import User
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

bcrypt = Bcrypt(app)
mail = Mail(app)


#Start of email authentication
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'brandon.andrew.reed@gmail.com'
app.config['MAIL_PASSWORD'] = 'Bronco2022*'
#app.config['MAIL_USE_TLS'] = 'False'
app.config['MAIL_USE_SSL'] = 'True'
mail = Mail(app)

s = URLSafeTimedSerializer(app.secret_key)
#   Create a token for security purposes
#   add the token to the url link
#   Check if email matches in the Database
#   If email is in database then send message to email address provided
#   redirect to the update password page

@app.route('/send_email', methods=['POST'])
def send_email():
    user = User.get_reset_email(request.form)
    email = request.form['email']
    token = s.dumps(email, salt=app.secret_key)
    print(email)
    print(token)
    if not user:
        flash("Email does not exist", "register")
        return redirect('/')
    if request.form['email'] == user.email:
        msg = Message('Confirm Email', sender='brandon.andrew.reed@gmail.com', recipients=['jonip46370@dmosoft.com'])
        link = url_for('update_password_page' ,id = user.id, token=token, _external=True)
        msg.body = "Yay it works!{}".format(link)
        mail.send(msg)
        return 'Sent'       

@app.route('/update_password_page/<int:id>/<token>')
def update_password_page(id, token):
    user = User.get_one(id)
    print(user.first_name + " " + user.last_name)
    try:
        email = s.loads(token, salt=app.secret_key, max_age=1000)
    except SignatureExpired:
        return '<h1>The token is expired</h1>'
    return render_template('')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/reset_email')
def reset_email():
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

    return redirect('/login_page')

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



