from flask import render_template, flash, session, request, redirect
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


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

