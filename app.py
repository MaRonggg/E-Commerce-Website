from pathlib import Path

from flask import render_template, session
from user_data.listing import bp as listing_bp
from user_data.sales_orders import bp as sales_orders_bp
from user_data.cart import cartbp as cart_bp
from Auth.register_account import register as reg
from Auth.login import auth as login
from flask import Flask
import database.database as db

app = Flask(__name__)
app.register_blueprint(listing_bp)
app.register_blueprint(sales_orders_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(reg)
app.register_blueprint(login)
app.secret_key = "aisjdioajdiowqjiodjasiojdioqw"


@app.route('/', methods=['GET'])
def main_page():
    # 判断用户是否登录
    if "email" in session:
        email = session['email']
        data = db.get_one_user(email)
        username = data['name']
        return render_template('main_page.html', username=username)
    return render_template('main_page.html')


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
    app.run(host='0.0.0.0', port=8000, debug=True)
