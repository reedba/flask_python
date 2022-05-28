from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.company_model import Company

@app.route("/add_company", methods=['POST'])
def add_company():
    print(request.form)
    data = {
        "company_name": request.form['company_name'],
        "website": request.form['website'],
        "user_id": request.form['user_id'],
    }
    Company.save_company(data)
    return redirect('/dashboard')


