
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask import render_template, flash, session, request, redirect, url_for

class Company:
    db = "resume_db"
    def __init__(self,data):
        self.id = data['id']
        self.company_name = data['company_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_company(cls, data):
        query = "INSERT INTO companies (company_name, website, user_id) VALUES (%(company_name)s, %(website)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def show_user_companies(cls, data):
        query = "SELECT * FROM companies WHERE user_id = %(id)s;"
        print(query, "*"*60)
        results = connectToMySQL(cls.db).query_db(query,data)
        
        companies = []
        for result in results:
            companies.append(cls(result))
        return companies
