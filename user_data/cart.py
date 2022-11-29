from flask import Blueprint, request, render_template
import html
from database.database import get_one_user, get_one_shopping_cart,create_shopping_cart,get_one_product, remove_product_from_shopping_cart, get_one_order, create_order,add_product_to_order, add_product_to_shopping_cart
from flask import render_template, session


cartbp = Blueprint('cart', __name__)



@cartbp.route('/shopping_cart', methods=['GET'])
def direct():
    if "email" in session:
        return render_template('user_cart.html')
    else:
        return render_template('login.html')


@cartbp.route('/displaycart', methods=['GET'])
def display():
        email = session['email']
        product_list = []
        if get_one_shopping_cart(email) is None:
            create_shopping_cart(email)
        else:
            a = get_one_shopping_cart(email)["product_id_list"]
            for aid in a:
                product_list.append(get_one_product(aid))
        return product_list

@cartbp.route('/add_to_cart', methods=['POST'])
def add_item():
    email = session['email']
    if get_one_shopping_cart(email) is None:
        create_shopping_cart(email)
    product_id = int(html.escape(request.form.get('add_id')))
    add_product_to_shopping_cart(product_id, user_email=email)
    a = get_one_shopping_cart(email)["product_id_list"]
    product_list = []
    for aid in a:
        product_list.append(get_one_product(aid))
    return product_list


@cartbp.route('/delete_from_cart', methods=['POST'])
def delete_item():
    email = session['email']
    product_id = int(html.escape(request.form.get('delete_id')))
    remove_product_from_shopping_cart(product_id, user_email=email)
    a = get_one_shopping_cart(email)["product_id_list"]
    product_list = []
    for aid in a:
        product_list.append(get_one_product(aid))
    return product_list


@cartbp.route('/checkout_cart', methods=['GET'])
def checkout():
    email = session['email']
    a = get_one_shopping_cart(email)["product_id_list"]
    if get_one_order(email) is None:
        create_order(email)

    for aid in a:
        add_product_to_order(aid, email)

    res = "Thank You"
    return res






