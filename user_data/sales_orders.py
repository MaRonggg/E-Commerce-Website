import html
from pathlib import Path

from flask import Blueprint, request, render_template, session, redirect, url_for
import database.database as db

bp = Blueprint('sales_orders', __name__)


@bp.route('/sales_page', methods=['GET'])
def sales_page():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    return render_template('sales.html')


@bp.route('/orders_page', methods=['GET'])
def orders_page():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    return render_template('orders.html')


@bp.route('/get_sales', methods=['GET'])
def get_sale():
    if 'email' in session:
        user_email = session['email']
        sales = db.get_all_sale(user_email)
        return list(sales)


@bp.route('/get_orders', methods=['GET'])
def get_orders():
    if 'email' in session:
        user_email = session['email']
        orders = db.get_all_order(user_email)
        return list(orders)


