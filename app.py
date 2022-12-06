import json
from pathlib import Path
from flask import request
from user_data.listing import bp as listing_bp
from user_data.sales_orders import bp as sales_orders_bp
from user_data.cart import cartbp as cart_bp
from Auth.register_account import register as reg
from Auth.login import auth as login
import database.database as db

from flask import Flask, render_template, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.register_blueprint(listing_bp)
app.register_blueprint(sales_orders_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(reg)
app.register_blueprint(login)
# app.secret_key = "aisjdioajdiowqjiodjasiojdioqw"

# app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins=['*',
                                               'http://localhost:8000',
                                               'http://localhost:8080'])


# @socketio.on('connect')
# def connect():
#     foo = request.args.get('foo')
#     print(foo)
#     print(foo)
#     print(foo)


# enable message show on webpage
@socketio.on('message', namespace='/')
def handleMessage(msg):
    print('Message: ' + msg)
    # get product id, get current user email
    # message is a price and id
    # use product id and price to change database
    if "email" in session:
        email = session['email']
        data = db.get_one_user(email)
        username = data['name']
        print(f'current user email would be {email}')
        print(f'the user name would be {username}')
        price_dict = json.loads(msg)
        price = price_dict['price']
        product_id = price_dict['product_id']
        print(f'price is {price} and product_id is {product_id}')
        print(f'user {email} offer price {price}')
    send(msg, broadcast=True)


@app.route('/', methods=['GET'])
def main_page():
    # 判断用户是否登录
    if "email" in session:
        email = session['email']
        data = db.get_one_user(email)
        username = data['name']
        return render_template('main_page.html', username=username)
    return render_template('main_page.html')


# @app.route('/hey', methods=['GET'])
# def page():
#     return render_template('main_page.html')

# @app.route('/websocket', methods=['GET', 'POST'])
# def pr():
#     print('enter the websocket')
#     return render_template('main_page.html')


@app.route('/script/<js_filename>', methods=['GET'])
def send_js(js_filename):
    with open(Path(__file__).parent / ('front_end/' + js_filename), 'rb') as js:
        return js.read()


@app.route('/cart.js', methods=['GET'])
def send_js1():
    with open(Path(__file__).parent / 'front_end/cart.js', 'rb') as js:
        return js.read()


# added path for login
# hey
# modify
#


@app.route('/image<image_id>', methods=['GET'])
def send_image(image_id):
    with open(Path(__file__).parent / ('images/image' + image_id + '.jpg'), 'rb') as image:
        return image.read()


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)
    # socketio.run(app, port=8000)
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
