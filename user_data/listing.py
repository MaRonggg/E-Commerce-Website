import html
from pathlib import Path

from flask import Blueprint, request, render_template
import database.database as db

bp = Blueprint('listing', __name__)


@bp.route('/create_page', methods=['GET'])
def create_listing_page():
    return render_template('create_listing.html')


@bp.route('/create', methods=['POST'])
def create_listing():
    name = html.escape(request.form.get('name'))
    description = html.escape(request.form.get('description'))
    price = request.form.get('price')
    image_name = db.create_product(name, price, description)

    image = request.files.get('image')
    image_path = Path(__file__).parent.parent / ('images/' + image_name + '.jpg')
    image.save(image_path)
    return 'created'


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

