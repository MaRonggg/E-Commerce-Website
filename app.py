from pathlib import Path

from flask import Flask, render_template
from user_data.listing import bp as listing_bp
from user_data.cart import cartbp as cart_bp
from flask import Flask, request


app = Flask(__name__)
app.register_blueprint(listing_bp)
app.register_blueprint(cart_bp)


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main_page.html')


@app.route('/listing.js', methods=['GET'])
def send_js():
    with open(Path(__file__).parent / 'front_end/listing.js', 'rb') as js:
        return js.read()


@app.route('/cart.js', methods=['GET'])
def send_js1():
    with open(Path(__file__).parent / 'front_end/cart.js', 'rb') as js:
        return js.read()

# added path for login
# hey


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
