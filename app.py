from pathlib import Path

from flask import render_template
from user_data.listing import bp as listing_bp
from user_data.cart import cartbp as cart_bp
from Auth.register_account import register as reg
from Auth.login import auth as login
from flask import Flask

app = Flask(__name__)
app.register_blueprint(listing_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(reg)
app.register_blueprint(login)
app.secret_key = "aisjdioajdiowqjiodjasiojdioqw"


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main_page.html')


@app.route('/main.js', methods=['GET'])
def send_main_js():
    with open(Path(__file__).parent / 'front_end/main.js', 'rb') as js:
        return js.read()


@app.route('/listing.js', methods=['GET'])
def send_listing_js():
    with open(Path(__file__).parent / 'front_end/listing.js', 'rb') as js:
        return js.read()


@app.route('/cart.js', methods=['GET'])
def send_js1():
    with open(Path(__file__).parent / 'front_end/cart.js', 'rb') as js:
        return js.read()

# added path for login
# hey
# modify
#


@app.route('/image/<image_id>', methods=['GET'])
def send_image(image_id):
    with open(Path(__file__).parent / ('images/image' + image_id + '.jpg'), 'rb') as image:
        return image.read()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
