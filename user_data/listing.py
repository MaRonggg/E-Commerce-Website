from flask import Blueprint, request, render_template
import database.database as db

bp = Blueprint('listing', __name__)


@bp.route('/create_page', methods=['GET'])
def create_listing_page():
    return render_template('create_listing.html')


@bp.route('/create', methods=['POST'])
def create_image():
    image = request.files.get('image')
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    db.create_product(name, price, image.filename, description)
    return 'created'


@bp.route('/get-all-products', methods=['GET'])
def get_all_products():
    all_products = db.get_all_products()
    return list(all_products)

