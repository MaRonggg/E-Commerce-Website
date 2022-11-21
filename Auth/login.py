import flask
from flask import render_template
from flask import request
from flask import session

auth = flask.Blueprint("auth",__name__)

@auth.route("/login",methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:

