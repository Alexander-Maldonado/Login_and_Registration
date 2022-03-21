from flask import redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def registration():
    if not User.validate_user(request.form):
        return redirect("/")
    data={
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":bcrypt.generate_password_hash(request.form["password"])
    }
    id = User.save(data)
    session["user_id"]=id
    return redirect("/welcome")

@app.route("/welcome")
def welcome():
    if "user_id" not in session:
        return redirect("/logout")
    data ={
        "id":session["user_id"]
    }
    return render_template("welcome.html",user=User.get_by_id(data))

@app.route("/logout")
def exit():
    session.clear()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    user=User.get_by_email(request.form)

    if not user:
        flash("Wrong Email")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Password does not match.")
        return redirect("/")
    session["user_id"]=user.id
    return redirect("/welcome")
