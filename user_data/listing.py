import html
from pathlib import Path

from flask import Blueprint, request, render_template, session, redirect, url_for
import database.database as db

bp = Blueprint('listing', __name__)


@bp.route('/create_page', methods=['GET'])
def create_listing_page():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    return render_template('create_listing.html')


@bp.route('/create', methods=['POST'])
def create_listing():
    if 'email' in session:
        email = session['email']

        name = html.escape(request.form.get('name'))
        description = html.escape(request.form.get('description'))

        if request.form.get('price') is not None:
            price = request.form.get('price')
            image_name = db.create_product(name, price, description)
        else:
            auction_deadline = request.form.get('auction_deadline')
            image_name = db.create_product(name, auction_deadline, description)

        image = request.files.get('image')
        image_path = Path(__file__).parent.parent / ('images/' + image_name + '.jpg')
        image.save(image_path)
    return "Created"


@bp.route('/get_all_products', methods=['GET'])
def get_all_products():
    all_products = db.get_all_products()
    return list(all_products)


@bp.route('/get_one_product/<product_id>', methods=['GET'])
def get_one_product(product_id):
    product = db.get_one_product(int(product_id))
    return product


@bp.route('/info_page/<product_id>', methods=['GET'])
def info_page(product_id):
    return render_template('product_info_page.html', product_id=product_id)


@bp.route('/buy_now/<product_id>', methods=['GET'])
def buy_now(product_id):
    if 'email' not in session:
        return 'not logged in'
    return 'logged in'





