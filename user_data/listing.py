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
        user_email = session['email']

        name = html.escape(request.form.get('name'))
        description = html.escape(request.form.get('description'))

        if request.form.get('price') is not None:
            price = request.form.get('price')
            product_id = db.create_product(name, price, description)
        else:
            auction_deadline = request.form.get('auction_deadline')
            product_id = db.create_product(name, auction_deadline, description)

        image = request.files.get('image')
        image_path = Path(__file__).parent.parent / ('images/image' + str(product_id) + '.jpg')
        image.save(image_path)

        if db.get_one_sale(user_email=user_email) is None:
            db.create_sale(user_email=user_email)
        db.add_product_to_on_sale(product_id=product_id, user_email=user_email)
        return 'Created'


@bp.route('/get_all_on_sale_products', methods=['GET'])
def get_all_on_sale_products():
    products = []
    data = db.get_all_sale()
    for piece in data:
        for product_id in piece['on_sale_products']:
            product = db.get_one_product(product_id)
            products.append(product)
    return products


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
        return 'Not Logged In'

    buyer_email = session['email']
    seller_email = None
    product_id = int(product_id)

    data = db.get_all_sale()
    flag = False
    for piece in data:
        for p_id in piece['on_sale_products']:
            if p_id == product_id:
                seller_email = piece['user_email']
                flag = True
                break
        if flag is True:
            break

    if flag is False:
        return 'Already Sold'

    db.move_product_on_sale_to_sold(product_id=product_id, user_email=seller_email)
    if db.get_one_order(user_email=buyer_email) is None:
        db.create_order(user_email=buyer_email)
    db.add_product_to_order(product_id=product_id, user_email=buyer_email)
    return 'Purchased'





