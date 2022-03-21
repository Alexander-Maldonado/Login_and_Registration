from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db ="login_register" 
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def gat_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db).query_db(query)
        user=[]
        for u in results:
            user.append(cls(u))
        return user

    @classmethod
    def get_one(cls,data):
        query= "SELECT * FROM user WHERE id = %(id)s;"
        results= connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return FALSE
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        query="SELECT * FROM user WHERE email =%(email)s"
        results=connectToMySQL(User.db).query_db(query,user)
        if len(results)>=1:
            flash("Email already registered to an account, please log in.")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Email not valid")
            is_valid=False
        if len(user["first_name"]) < 2:
            flash("First name must be at least 2 characters long.")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last name must be at least 2 characters long.")
            is_valid = False
        if len(user["email"])<1:
            flash("Email is not valid.")
            is_valid = False
        if len(user["password"])<8:
            flash("Password must be at least 8 characters long.")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match")
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.db).query_db(query,data)