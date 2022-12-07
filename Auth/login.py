import flask
from flask import render_template, flash, redirect, url_for
from flask import request
from flask import session
from database import database
from bcrypt import checkpw, gensalt, hashpw

from datetime import timedelta
from flask import session, app


auth = flask.Blueprint("auth", __name__)
salt = gensalt()

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("psw")
        if not email or not password:
            flash('Invalid input.')
            return redirect(url_for('auth.login'))
        user = database.user_collection.find_one({"email": email})
        if not user:
            flash('Email not Found.')
            return redirect(url_for('auth.login'))
        else:
            if not checkpw(password.encode('utf-8'), user.get("password")):
                flash('Incorrect password.')
                return redirect(url_for('auth.login'))
            else:
                session['email'] = email
                # # add  5 minutes time for session to expire
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=15)
                # show message
                flash('Login success.')
                return render_template("main_page.html", username=email, hide=True)
    else:
        return render_template("login.html")

@auth.route("/logout", methods=['GET', 'POST'])
def logout():
        if 'email' in session:
            session.pop('email', None)
            return render_template("main_page.html", hide=False)
        else:
            return '<p>user already logout</p>'





