from flask import Blueprint, render_template, session, redirect, url_for
import database.database as db

bp = Blueprint('sales_orders', __name__)


@bp.route('/sales_page', methods=['GET'])
def sales_page():
    if not session or 'email' not in session:
        return redirect(url_for('auth.login'))
    return render_template('sales.html')


@bp.route('/orders_page', methods=['GET'])
def orders_page():
    if not session or 'email' not in session:
        return redirect(url_for('auth.login'))
    return render_template('orders.html')


@bp.route('/get_sales', methods=['GET'])
def get_sale():
    if session and 'email' in session:
        user_email = session['email']

        for_sale = []
        sold = []
        products = {'for_sale': for_sale, 'sold': sold}

        data = db.get_one_sale(user_email=user_email)

        if data is not None:
            for product_id in data['on_sale_products']:
                product = db.get_one_product(product_id)
                for_sale.append(product)

            for product_id in data['sold_products']:
                product = db.get_one_product(product_id)
                sold.append(product)

        return products


@bp.route('/get_orders', methods=['GET'])
def get_orders():
    if session and 'email' in session:
        user_email = session['email']

        products = []

        data = db.get_one_order(user_email=user_email)

        if data is not None:
            for product_id in data['product_id_list']:
                product = db.get_one_product(product_id)
                products.append(product)

        return products


