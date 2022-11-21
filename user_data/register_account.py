from flask import Blueprint, request, render_template
import json
from database.database import get_one_user, get_one_shopping_cart

#from database import db

register = Blueprint('register', __name__)
#listing_collection = db['listing']


@register.route('/register', methods=['GET'])
def reg():
    return render_template('register_account.html')
