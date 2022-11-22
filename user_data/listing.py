from pathlib import Path

from flask import Blueprint, request, render_template
import database.database as db

bp = Blueprint('listing', __name__)


image_id = 1


@bp.route('/create_page', methods=['GET'])
def create_listing_page():
    return render_template('create_listing.html')


@bp.route('/create', methods=['POST'])
def create_listing():
    global image_id
    image = request.files.get('image')
    image_path = str(Path(__file__).parent.parent / ('images/image' + str(image_id) + '.jpg'))
    image_id += 1
    image.save(image_path)

    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    db.create_product(name, price, image_path, description)
    return 'created'


@bp.route('/get-all-products', methods=['GET'])
def get_all_products():
    all_products = db.get_all_products()
    return list(all_products)

