import flask
from flask import render_template, flash, redirect, url_for
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
            flash('Email not Found.')
            return redirect(url_for('login'))
        else:
            if not checkpw(hashpw(password.encode('utf-8'), salt), user.get("password")):
                flash('Incorrect password.')
                return redirect(url_for('login'))
            else:
                session["email"] = email
                flash('Login success.')
                return render_template("logined.html", email=email)
    return render_template("login.html")




