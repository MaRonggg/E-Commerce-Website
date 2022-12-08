import datetime
import html
from pathlib import Path

from flask import Blueprint, request, render_template, session, redirect, url_for
import database.database as db

bp = Blueprint('listing', __name__)


@bp.route('/create_page', methods=['GET'])
def create_listing_page():
    if not session or 'email' not in session:
        return redirect(url_for('auth.login'))
    return render_template('create_listing.html')


@bp.route('/create', methods=['POST'])
def create_listing():
    if session and 'email' in session:
        user_email = session['email']

        name = html.escape(request.form.get('name'))
        description = html.escape(request.form.get('description'))

        request.headers

        if request.form.get('auction_deadline') is None:
            price = request.form.get('price')
            product_id = db.create_product(product_name=name, product_price=price, product_description=description)
        else:
            auction_deadline = request.form.get('auction_deadline')
            # print(auction_deadline)
            # print(datetime.datetime.strptime(auction_deadline,'%Y-%m-%dT%H:%M'))
            # print(type(auction_deadline))
            # convert auction_deadline string to datetime.datetime
            auction_deadline_datetime = datetime.datetime.strptime(auction_deadline,'%Y-%m-%dT%H:%M')
            product_id = db.create_product(product_name=name, product_price=-1,
                                           product_description=description,
                                           auction_end_time=auction_deadline_datetime)

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
            # check product auction end time
            current_time = datetime.datetime.now()
            auction_end_time = product['auction_end_time']
            if auction_end_time and auction_end_time > current_time:
                products.append(product)
            elif not auction_end_time:
                # item is not on auction, show it anyway
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
def buy_now(product_id, buyer_email=None):
    if not session or 'email' not in session:
        return 'Not Logged In'

    if buyer_email is None:
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


@bp.route('/auction_page/<product_id>', methods=['GET'])
def auction_page(product_id):
    if not session or 'email' not in session:
        return redirect(url_for('auth.login'))
    return render_template('auction_page.html', product_id=product_id)





