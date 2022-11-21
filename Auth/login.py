import flask
from flask import render_template, flash, redirect, url_for
from flask_login import login_user
from flask import request
from flask import session
from database import database
from bcrypt import checkpw, gensalt, hashpw

auth = flask.Blueprint("auth", __name__)
salt = gensalt()

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("psw")
        if not email or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        user = database.user_collection.find_one({"email": email})
        if not user:
            flash('Invalid email.')
            return redirect(url_for('login'))
        if not checkpw(hashpw(password.encode('utf-8'), salt), user.get("password")):
            flash('Incorrect password.')
            return redirect(url_for('login'))
        else:
            login_user()
            flash('Login success.')
            return redirect(url_for('/'))
    return render_template("login.html")




