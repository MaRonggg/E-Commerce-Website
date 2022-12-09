import datetime
import json
from pathlib import Path
from flask import request, Response
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
                                               'http://localhost:8080',
                                               'https://localhost',
                                               'https://165.22.4.4',
                                               'https://165.22.4.4:8080',
                                               'https://165.22.4.4:8000'])


# enable message show on webpage
@socketio.on('message')
def handleMessage(msg):
    if session and ("email" in session):
        user_email = session['email']
        product_price = float(json.loads(msg)['price'])
        product_id = int(json.loads(msg)['product_id'])

        # update_result returns bool, true -> eligible update
        update_result = db.update_auction_item(user_email,
                                               product_id,
                                               product_price,
                                               datetime.datetime.now())
        if update_result == 'ok':
            print('handleMessage OK')

            product_name = db.get_one_product(product_id)['product_name']
            username = db.get_one_user(user_email)['name']
            # offer_message = f'{user_email} offered ${product_price} for {product_name}!'
            # print(offer_message)
            # send(offer_message, broadcast=True)
            data = {'username': username, 'productName': product_name, 'price': product_price}
            send(data, broadcast=True)
        elif update_result == 'invalid price':
            print('handleMessage invalid price')
            # check if the time expired, if it is
            # show a different message to inform user

            # also, add the order
            # no broadcast, only seen by one user
            send(update_result, broadcast=False)
        elif update_result == 'expired':
            print('handleMessage OK')
            # no broadcast, only seen by one user
            send(update_result, broadcast=False)


@app.route('/', methods=['GET'])
def main_page():
    # 判断用户是否登录
    if session and "email" in session:
        email = session['email']
        data = db.get_one_user(email)
        username = data['name']
        return render_template('main_page.html', username=username, hide=True)
    return render_template('main_page.html', hide=False)


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


@app.route('/image<image_id>', methods=['GET'])
def send_image(image_id):
    with open(Path(__file__).parent / ('images/image' + image_id + '.jpg'), 'rb') as image:
        return image.read()


@app.route('/style.css', methods=['GET'])
def css():
    with open(f'style.css', 'r') as f:
        css_file = f.read()
    return Response(css_file, mimetype='text/css')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)
    # socketio.run(app, port=8000)
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)


