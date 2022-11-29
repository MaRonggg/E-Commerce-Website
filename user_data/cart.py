from flask import Blueprint, request, render_template
import html
from database.database import get_one_user, get_one_shopping_cart,create_shopping_cart,get_one_product, remove_product_from_shopping_cart, get_one_order, create_order,add_product_to_order, add_product_to_shopping_cart
from flask import render_template, session
import database.database as db

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


    return "added"


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

        remove_product_from_shopping_cart(aid, user_email=email)
        buyer_email = session['email']
        seller_email = None
        product_id = int(aid)
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

    res = "Thank You"
    return res





