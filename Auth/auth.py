import flask
from flask import render_template, flash, redirect, url_for
from flask_login import login_user
from flask import request
from flask import session
from database import database
from werkzeug.security import check_password_hash

auth = flask.Blueprint("auth",__name__)

@auth.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        user = database.user_collection.find_one({"email": username})
        if not user:
            flash('Invalid username.')
            return redirect(url_for('login'))
        if user.get("password") != check_password_hash('hash', password):
            flash('Incorrect password.')
            return redirect(url_for('login'))
        else:
            login_user()
            flash('Login success.')
            return redirect(url_for('/'))
    return render_template("login.html")


@auth.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register_account.html")

