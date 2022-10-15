from flask import Blueprint, request, render_template
from database import db

bp = Blueprint('listing', __name__)
listing_collection = db['listing']


@bp.route('/create_page', methods=['GET'])
def create_listing_page():
    return render_template('create_listing.html')


@bp.route('/create', methods=['POST'])
def create_image():
    image = request.files.get('image')
    description = request.form.get('description')
    price = request.form.get('price')
    # db.save_file(image.filename, image)
    # listing_collection.insert_one({'image': image.filename, 'description': description, 'price': price})
    print(image)
    print(description)
    print(price)
    return 'created'
