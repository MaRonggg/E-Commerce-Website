from flask import Blueprint, request, render_template, redirect, url_for, flash
import bcrypt
from database import database

from Auth.html_injection_replace import escape_html_chars

import json
from database.database import get_one_user, get_one_shopping_cart
import  database.database as db
# from database import db
salt = bcrypt.gensalt()
register = Blueprint('register', __name__)


# listing_collection = db['listing']


@register.route('/register', methods=['GET','POST'])
def reg():
    if request.method == "GET":
        return render_template('register_account.html')
    elif request.method == 'POST':
        # after submit form, store the value into database
        # use the lab for id to find the part
        email = request.form.get("email")
        pas1 = request.form.get("psw")
        pas2 = request.form.get("psw2")
        # escape characters to avoid injection attack
        email = escape_html_chars(email)
        pas1 = escape_html_chars(pas1)
        pas2 = escape_html_chars(pas2)
        # compare password
        if pas2 != pas1:
            # message did not appear
            flash('Passwords should be same!')
            return redirect(url_for('register.reg'))
        password = bcrypt.hashpw(pas1.encode('utf-8'), salt)
        name = request.form.get("name")
        name = escape_html_chars(name)

        print(f'reg_info being called')
        print(request)
        print(f'username would be {name}')
        print(f'password would be {password}')
        database.create_user_account(email, password, name)
        return redirect(url_for('auth.login'))




