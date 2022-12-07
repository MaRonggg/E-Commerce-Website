import flask
from flask import render_template, flash, redirect, url_for
from flask import request
from flask import session
from database import database
from bcrypt import checkpw, gensalt, hashpw

from datetime import timedelta
from flask import session, app

# escape characters
from Auth.html_injection_replace import escape_html_chars


auth = flask.Blueprint("auth", __name__)
salt = gensalt()

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        email = escape_html_chars(email)
        password = request.form.get("psw")
        password = escape_html_chars(password)

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
                # show message
                flash('Login success.')
                return render_template("main_page.html", username=email, hide=True)
    else:
        return render_template("login.html")

@auth.route("/logout", methods=['GET'])
def logout():
    if 'email' in session:
        session.clear()
        return render_template("main_page.html", hide=False)






