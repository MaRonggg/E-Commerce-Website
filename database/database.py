from pathlib import Path

from flask_pymongo import MongoClient
import bcrypt

# works for local
# mongo_client = MongoClient('mongodb://localhost:27017')
# works for docker
mongo_client = MongoClient("mongo")
db = mongo_client['5bytes']

# User_accounts(
#     user_id: int, password: bytes, email: str, name: str,
#     address1: str, address2: str, city: str, state: str, zip: str,
#     sale_id: int, order_id: int, cart_id: int
# )
# primary_key -> email, foreign_key -> sale_id, order_id, cart_id
user_collection = db["User_account"]
# store the last id
user_id_collection = db["user_id"]

# Product (
#     product_id: int, product_name: str, product_price: double,
#     product_images: list[Path], product_description: str
# )
# primary_key -> product_id, foreign_key -> none
product_collection = db["product"]
product_id_collection = db["product_id"]

# Sale(sale_id: int, user_email: str, product_id_list: list[int])
# primary_key -> sale_id, foreign_key -> user_email
sale_collection = db["sale"]
sale_id_collection = db["sale_id"]

# Order(order_id: int, user_email: str, product_id_list: list[int])
# primary_key -> order_id, foreign_key -> user_email
order_collection = db["order"]
order_id_collection = db["order_id"]

# Shopping_cart(cart_id: int, user_email: str, product_id_list: list[int])
# primary_key -> cart_id, foreign_key -> user_email
shopping_cart_collection = db["shopping_cart"]
shopping_cart_id_collection = db["shopping_cart_id"]


# ------------ user_collection methods --------------------
# User_accounts(
#     user_id: int, password: str, email: str, name: str,
#     address1: str, address2: str, city: str, state: str, zip: str,
#     sale_id: int, order_id: int, cart_id: int
# )


def create_user_account(email: str, password: bytes, name: str):
    user_dict = {
        "_id": __get_next_user_id(),
        "email": email,
        "password": password,
        "name": name,
        "address1": "", "address2": "", "city": "", "state": "", "zip_code": "",
        "sale_id": -1, "order_id": -1, "cart_id": -1
    }
    insert_result = user_collection.insert_one(user_dict)
    # print(insert_result.inserted_id)
    return get_one_user(email)


def update_user_address(email: str, password: bytes,
                        address1: str, address2: str,
                        city: str, state: str, zip_code: str):
    if verify_user_password(email, password):
        user_collection.update_one({"email": email}, {"$set": {"address1": address1}})
        user_collection.update_one({"email": email}, {"$set": {"address2": address2}})
        user_collection.update_one({"email": email}, {"$set": {"city": city}})
        user_collection.update_one({"email": email}, {"$set": {"state": state}})
        user_collection.update_one({"email": email}, {"$set": {"zip_code": zip_code}})
        return "setting address successful"
    else:
        return "password mismatching"


# update sale_id, order_id, and cart_id.
# update_user_relational_id(u_id, password, order_id = some_o_id) to update specific id
def update_user_relational_id(email: str, password: bytes,
                              sale_id: int = None,
                              order_id: int = None,
                              cart_id: int = None):
    if verify_user_password(email, password):
        return "password mismatching"
    if sale_id is not None:
        user_collection.update_one({"email": email}, {"$set": {"sale_id": sale_id}})
    if order_id is not None:
        user_collection.update_one({"email": email}, {"$set": {"order_id": order_id}})
    if cart_id is not None:
        user_collection.update_one({"email": email}, {"$set": {"cart_id": cart_id}})


# reset password
def update_user_password(email: str, password: bytes, new_password: str):
    if verify_user_password(email, password):
        user_collection.update_one({"email": email}, {"$set": {"password": new_password}})
        return "password reset successful"
    else:
        return "password mismatching"


def verify_user_password(email: str, entered_password: bytes):
    user_account = user_collection.find_one({"email": email})
    if user_account is None:
        return False
    return bcrypt.checkpw(entered_password, user_account["password"])


# return one row data
def get_one_user(email: str):
    return user_collection.find_one({"email": email})


# return all rows as list[row]
def get_all_users():
    return [user for user in user_collection.find({})]


# ------------ user_collection methods end --------------------
# ------------ product_collection methods --------------------
# Product (
#     product_id: int, product_name: str, product_price: double,
#     product_image: Path, product_description: str
# )


def create_product(product_name: str, product_price: float,
                   product_description: str = ""):
    product_id = __get_next_product_id()
    product_image_name = "image" + str(product_id)
    product_dict = {
        "_id": product_id,
        "product_name": product_name,
        "product_price": product_price,
        "product_image": product_image_name,
        "product_description": product_description
    }
    insert_result = product_collection.insert_one(product_dict)
    return product_image_name


def update_product_price(product_id: int, product_price: float):
    product_collection.update_one({"_id": product_id}, {"$set": {"product_price": product_price}})
    return "price update successful"


# optional arg image_index; the insert method uses as append by default
def update_product_image(product_id: int, image_path: Path):
    product_collection.update_one({"_id": product_id}, {"$set": {"product_images": image_path}})
    return "image added"


# optional arg image_index; the method remove image by index. remove_all if no index
def remove_product_image(product_id: int, image_index: int = None):
    product_collection.update_one({"_id": product_id}, {"$set": {"product_images": 'images/default.jpeg'}})
    return "image removed"


def update_product_description(product_id: int, product_description: str):
    product_collection.update_one({"_id": product_id}, {"$set": {"product_description": product_description}})
    return "description update successful"


def delete_one_product(product_id: int):
    product_collection.delete_one({"_id": product_id})
    product_id_collection.delete_one({"_id": product_id})


def get_one_product_by_imagename(product_image_name: str):
    return product_collection.find_one({"product_image": product_image_name})


# return one row data
def get_one_product(product_id: int):
    return product_collection.find_one({"_id": product_id})


# return all rows as list[row]
def get_all_products():
    return [product for product in product_collection.find({})]


# ------------ product_collection methods end --------------------
# ------------ sale_collection methods --------------------
# Sale(sale_id: int, user_email: str, on_sale_p_id: list[int], sold_p_id: list[int])
def create_sale(user_email: str,
                on_sale_p_id: list = None,
                sold_p_id: list = None):
    if on_sale_p_id is None:
        on_sale_p_id = []
    if sold_p_id is None:
        sold_p_id = []
    sale_dict = {
        "_id": __get_next_sale_id(),
        "user_email": user_email,
        "on_sale_products": on_sale_p_id,  # on_sale_p_id -> on sale product id list
        "sold_products": sold_p_id  # sold_p_id -> sold product id list
    }
    sale_collection.insert_one(sale_dict)
    return get_one_sale(user_email)


# use either sale_id or user_email to access
def add_product_to_on_sale(product_id: int,
                           user_email: str = None,
                           sale_id: int = None):
    if sale_id is not None:
        p_list = get_one_sale(sale_id=sale_id)["on_sale_products"]
        p_list.append(product_id)
        sale_collection.update_one({"_id": sale_id},
                                   {"$set": {"on_sale_products": p_list}})
        return "product added"
    if user_email is not None:
        p_list = get_one_sale(user_email=user_email)["on_sale_products"]
        p_list.append(product_id)
        sale_collection.update_one({"user_email": user_email},
                                   {"$set": {"on_sale_products": p_list}})
        return "product added"


# use either sale_id or user_email to access
def add_product_to_sold(product_id: int,
                        user_email: str = None,
                        sale_id: int = None):
    if sale_id is not None:
        p_list = get_one_sale(sale_id=sale_id)["sold_products"]
        p_list.append(product_id)
        sale_collection.update_one({"_id": sale_id},
                                   {"$set": {"sold_products": p_list}})
        return "product added"
    if user_email is not None:
        p_list = get_one_sale(user_email=user_email)["sold_products"]
        p_list.append(product_id)
        sale_collection.update_one({"user_email": user_email},
                                   {"$set": {"sold_products": p_list}})
        return "product added"


# use either sale_id or user_email to access
def move_product_on_sale_to_sold(product_id: int,
                                 user_email: str = None,
                                 sale_id: int = None):
    if sale_id is not None:
        add_product_to_sold(product_id, sale_id=sale_id)
        remove_product_from_on_sale(product_id, sale_id=sale_id)
    if user_email is not None:
        add_product_to_sold(product_id, user_email=user_email)
        remove_product_from_on_sale(product_id, user_email=user_email)


# remove the first matching element
# use either sale_id or user_email to access
def remove_product_from_on_sale(product_id: int,
                                sale_id: int = None,
                                user_email: str = None):
    if sale_id is not None:
        p_list = get_one_sale(sale_id=sale_id)["on_sale_products"]
        p_list.remove(product_id)
        sale_collection.update_one({"_id": sale_id},
                                   {"$set": {"on_sale_products": p_list}})
        return "product removed"
    if user_email is not None:
        p_list = get_one_sale(user_email=user_email)["on_sale_products"]
        p_list.remove(product_id)
        sale_collection.update_one({"user_email": user_email},
                                   {"$set": {"on_sale_products": p_list}})
        return "product removed"


# use either sale_id or user_email to access
def remove_product_from_sold(product_id: int,
                             sale_id: int = None,
                             user_email: str = None):
    if sale_id is not None:
        p_list = get_one_sale(sale_id=sale_id)["sold_products"]
        p_list.remove(product_id)
        sale_collection.update_one({"_id": sale_id},
                                   {"$set": {"sold_products": p_list}})
        return "product removed"
    if user_email is not None:
        p_list = get_one_sale(user_email=user_email)["sold_products"]
        p_list.remove(product_id)
        sale_collection.update_one({"user_email": user_email},
                                   {"$set": {"sold_products": p_list}})
        return "product removed"


# return one row data
# use either sale_id or user_email to access
def get_one_sale(user_email: str = None, sale_id: int = None):
    if sale_id is not None:
        return sale_collection.find_one({"_id": sale_id})
    if user_email is not None:
        return sale_collection.find_one({"user_email": user_email})


# return all rows as list[row]
def get_all_sale():
    return [sale for sale in sale_collection.find({})]


# ------------ sale_collection methods end --------------------
# ------------ order_collection methods --------------------
# Order(order_id: int, user_email: str, product_id_list: list[int])
def create_order(user_email: str = None, product_id_list=None):
    if product_id_list is None:
        product_id_list = []
    sale_dict = {
        "_id": __get_next_order_id(),
        "user_email": user_email,
        "product_id_list": product_id_list
    }
    insert_result = order_collection.insert_one(sale_dict)
    return get_one_order(insert_result.inserted_id)


# use either order_id or user_email to access
def add_product_to_order(product_id: int,
                        user_email: str = None,
                        order_id: int = None):
    if order_id is not None:
        p_list = get_one_order(order_id=order_id)["product_id_list"]
        p_list.append(product_id)
        sale_collection.update_one({"_id": order_id},
                                   {"$set": {"product_id_list": p_list}})
        return "product added"
    if user_email is not None:
        p_list = get_one_order(user_email=user_email)["product_id_list"]
        p_list.append(product_id)
        sale_collection.update_one({"user_email": user_email},
                                   {"$set": {"product_id_list": p_list}})
        return "product added"


# remove the first matching element
# use either order_id or user_email to access
def remove_product_from_order(product_id: int, user_email: str = None, order_id: int = None):
    if order_id is not None:
        p_list = get_one_order(order_id=order_id)["product_id_list"]
        p_list.remove(product_id)
        sale_collection.update_one({"_id": order_id},
                                   {"$set": {"product_id_list": p_list}})
        return "product removed"
    if user_email is not None:
        p_list = get_one_order(user_email=user_email)["product_id_list"]
        p_list.remove(product_id)
        sale_collection.update_one({"user_email": user_email},
                                   {"$set": {"product_id_list": p_list}})
        return "product removed"


# return one row data
# use either order_id or user_email to access
def get_one_order(user_email: str = None, order_id: int = None):
    if user_email is not None:
        return order_collection.find_one({"user_email": user_email})
    if order_id is not None:
        return order_collection.find_one({"_id": order_id})


# return all rows as list[row]
def get_all_order():
    return [order for order in order_collection.find({})]


# ------------ order_collection methods end --------------------
# ------------ shopping_cart_collection methods --------------------
# Shopping_cart(cart_id: int, user_email: str, product_id_list: list[int])
def create_shopping_cart(user_email: str, product_id_list=None):
    if product_id_list is None:
        product_id_list = []
    shopping_cart_dict = {
        "_id": __get_next_shopping_cart_id(),
        "user_email": user_email,
        "product_id_list": product_id_list
    }
    insert_result = shopping_cart_collection.insert_one(shopping_cart_dict)
    return get_one_sale(insert_result.inserted_id)


# use either shopping_cart_id or user_email to access
def add_product_to_shopping_cart(product_id: int,
                                 shopping_cart_id: int = None,
                                 user_email: str = None):
    if shopping_cart_id is not None:
        p_list = get_one_shopping_cart(shopping_cart_id=shopping_cart_id)["product_id_list"]
        p_list.append(product_id)
        shopping_cart_collection.update_one({"_id": shopping_cart_id},
                                   {"$set": {"product_id_list": p_list}})
        return "product added"
    if user_email is not None:
        p_list = get_one_shopping_cart(user_email=user_email)["product_id_list"]
        p_list.append(product_id)
        shopping_cart_collection.update_one({"user_email": user_email},
                                   {"$set": {"product_id_list": p_list}})
        return "product added"


# remove the first matching element
# use either shopping_cart_id or user_email to access
def remove_product_from_shopping_cart(product_id: int,
                                      shopping_cart_id: int = None,
                                      user_email: str = None):
    if shopping_cart_id is not None:
        p_list = get_one_shopping_cart(shopping_cart_id=shopping_cart_id)["product_id_list"]
        p_list.remove(product_id)
        shopping_cart_collection.update_one({"_id": shopping_cart_id},
                                   {"$set": {"product_id_list": p_list}})
        return "product removed"
    if user_email is not None:
        p_list = get_one_shopping_cart(user_email=user_email)["product_id_list"]
        p_list.remove(product_id)
        shopping_cart_collection.update_one({"user_email": user_email},
                                   {"$set": {"product_id_list": p_list}})
        return "product removed"
#

# return one row data
# use either shopping_cart_id or user_email to access
def get_one_shopping_cart(user_email: str = None,
                          shopping_cart_id: int = None):
    if shopping_cart_id is not None:
        return shopping_cart_collection.find_one({"_id": shopping_cart_id})
    if user_email is not None:
        return shopping_cart_collection.find_one({"user_email": user_email})


# return all rows as list[row]
def get_all_shopping_cart():
    return [shopping_cart for shopping_cart in shopping_cart_collection.find({})]


# ------------ shopping_cart_collection methods end --------------------

# ------------ Private method --------------------
def __get_next_user_id():
    return __get_next_id_for(user_id_collection)


def __get_next_product_id():
    return __get_next_id_for(product_id_collection)


def __get_next_sale_id():
    return __get_next_id_for(sale_id_collection)


def __get_next_order_id():
    return __get_next_id_for(order_id_collection)


def __get_next_shopping_cart_id():
    return __get_next_id_for(shopping_cart_id_collection)


def __get_next_id_for(collection):
    id_object = collection.find_one({})
    if id_object:
        next_id = int(id_object["last_id"]) + 1
        collection.update_one({}, {"$set": {"last_id": next_id}})
        return next_id
    else:
        collection.insert_one({"last_id": 1})
        return 1
