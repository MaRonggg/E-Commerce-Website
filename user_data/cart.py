from flask import Blueprint, request, render_template
import json
from database.database import get_one_user, get_one_shopping_cart

#from database import db

cartbp = Blueprint('cart', __name__)
#listing_collection = db['listing']


@cartbp.route('/shopping_cart', methods=['GET'])
def direct():
    return render_template('cart.html')

@cartbp.route('/guest', methods=['GET'])
def redirect():
    return render_template('guest_cart.html')

@cartbp.route('/showcart', methods=['POST'])

def showcart():
    account = request.files.get('id')
    nav = json.loads(get_one_shopping_cart(account).decode())
    return render_template(
        'user_cart.html',
        nav=nav

    )
@cartbp.route('/checkinfor', methods=['GET'])
def checkinfor():
    account = request.files.get('id')

    infor = json.loads(get_one_user(account).decode())
    return infor



