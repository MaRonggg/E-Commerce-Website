from flask import Blueprint, request, render_template

from database.database import get_one_user, get_one_shopping_cart,create_shopping_cart,get_one_product, remove_product_from_shopping_cart
from flask import render_template, session


cartbp = Blueprint('cart', __name__)



@cartbp.route('/shopping_cart', methods=['GET'])
def direct():
    if "email" in session:
        email = session['email']
        image_list = []
        if get_one_shopping_cart(email) is None:
            create_shopping_cart(email)

        else:
            a = get_one_shopping_cart(email)["product_id_list"]
            for aid in a:
                image_list.append(get_one_product(aid)["product_image"])
        return render_template(
            'user_cart.html',
            nav=image_list
        )
    else:
        return render_template('login.html')


@cartbp.route('/delete_from_cart', methods=['POST'])
def delete_item(product_image):
    aid = get_one_product_by_imagename(product_image)["_id"]
    email = session['email']
    remove_product_from_shopping_cart(aid, user_email=email)
    a = get_one_shopping_cart(email)["product_id_list"]
    image_list = []
    for aid in a:
        image_list.append(get_one_product(aid)["product_image"])
    return render_template(
        'user_cart.html',
        nav=image_list
    )

@cartbp.route('/checkout_cart', methods=['GET'])
def checkout():
    email = session['email']
    a = get_one_shopping_cart(email)["product_id_list"]
    for aitem in a:
        remove_product_from_shopping_cart(aitem, user_email=email)
    return render_template(
        'user_cart.html',
        nav=[]
    )

@cartbp.route('/guest', methods=['GET'])
def redirect():
    return render_template('guest_cart.html')




