from pathlib import Path

from flask_pymongo import MongoClient

mongo_client = MongoClient('mongo')
db = mongo_client['5bytes']

# User_accounts(
#     user_id: int, password: str, email: str, name: str,
#     address1: str, address2: str, city: str, state: str, zip: str,
#     sale_id: int, order_id: int, cart_id: int
# )
user_collection = db["User_account"]
# store the last id
user_id_collection = db["user_id"]

# Product (
#     product_id: int, product_name: str, product_price: double,
#     product_images: list[Path], product_description: str
# )
product_collection = db["product"]
product_id_collection = db["product_id"]

# Sale(sale_id: int, user_id: int, product_id_list: list[int])
# primary_key -> sale_id, foreign_key -> user_id
sale_collection = db["sale"]
sale_id_collection = db["sale_id"]

# Order(order_id: int, user_id: int, product_id_list: list[int])
# primary_key -> order_id, foreign_key -> user_id
order_collection = db["order"]
order_id_collection = db["order_id"]

# Shopping_cart(cart_id: int, user_id: int, product_id_list: list[int])
# primary_key -> cart_id, foreign_key -> user_id
shopping_cart_collection = db["shopping_cart"]
shopping_cart_id_collection = db["shopping_cart_id"]


# ------------ user_collection methods --------------------
# User_accounts(
#     user_id: int, password: str, email: str, name: str,
#     address1: str, address2: str, city: str, state: str, zip: str,
#     sale_id: int, order_id: int, cart_id: int
# )

def get_next_user_id():
    return __get_next_id_for(user_id_collection)


def create_user_account(user_id: int, email: str, password: str, name: str):
    user_dict = {
        "_id": user_id,
        "email": email,
        "password": password,
        "name": name,
        "address1": "", "address2": "", "city": "", "state": "", "zip_code": "",
        "sale_id": -1, "order_id": -1, "cart_id": -1
    }
    insert_result = user_collection.insert_one(user_dict)
    # print(insert_result.inserted_id)
    return get_one_user(insert_result.inserted_id)


def update_user_address(user_id: int, password: str,
                        address1: str, address2: str,
                        city: str, state: str, zip_code: str):
    user_password = get_one_user(user_id)["password"]
    if user_password == password:
        user_collection.update_one(
            {"_id": user_id},
            {"$set": {"address1": address1}},
            {"$set": {"address2": address2}},
            {"$set": {"city": city}},
            {"$set": {"state": state}},
            {"$set": {"zip_code": zip_code}}
        )
        return "setting address successful"
    else:
        return "password mismatching"


# update sale_id, order_id, and cart_id.
# update_user_relational_id(u_id, password, order_id = some_o_id) to update specific id
def update_user_relational_id(user_id: int, password: str,
                              sale_id: int = None,
                              order_id: int = None,
                              cart_id: int = None):
    user_password = get_one_user(user_id)["password"]
    if user_password != password:
        return "password mismatching"
    if sale_id is not None:
        user_collection.update_one({"_id": user_id}, {"$set": {"sale_id": sale_id}})
    if order_id is not None:
        user_collection.update_one({"_id": user_id}, {"$set": {"order_id": order_id}})
    if cart_id is not None:
        user_collection.update_one({"_id": user_id}, {"$set": {"cart_id": cart_id}})


# reset password
def update_user_password(user_id: int, old_password: str, new_password: str):
    user_password = get_one_user(user_id)["password"]
    if user_password == old_password:
        user_collection.update_one(
            {"_id": user_id},
            {"$set": {"password": new_password}}
        )
        return "password reset successful"
    else:
        return "password mismatching"


def get_one_user(user_id: int):
    return user_collection.find_one({"_id": user_id})


def get_all_users():
    return [user for user in user_collection.find({})]


# ------------ user_collection methods end --------------------
# ------------ product_collection methods --------------------
# Product (
#     product_id: int, product_name: str, product_price: double,
#     product_images: list[Path], product_description: str
# )

def get_next_product_id():
    return __get_next_id_for(product_id_collection)


def create_product(product_id: int, product_name: str, product_price: float,
                   product_images: list[Path] = None, product_description: str = ""):
    if product_images is None:
        product_images = []
    product_dict = {
        "_id": product_id,
        "product_name": product_name,
        "product_price": product_price,
        "product_images": product_images,
        "product_description": product_description
    }
    insert_result = product_collection.insert_one(product_dict)
    # print(insert_result.inserted_id)
    return get_one_product(insert_result.inserted_id)


def update_product_price(product_id: int, product_price: float):
    product_collection.update_one({"_id": product_id}, {"$set": {"product_price": product_price}})
    return "price update successful"


# optional arg image_index; the insert method uses as append by default
def insert_one_product_image(product_id: int, image_path: Path, image_index: int = None):
    old_product_images = get_one_product(product_id)["product_images"]
    if image_index is None:
        new_product_images = old_product_images.append(image_path)
        product_collection.update_one({"_id": product_id},
                                      {"$set": {"product_images": new_product_images}})
    else:
        new_product_images = old_product_images.insert(image_index, image_path)
        product_collection.update_one({"_id": product_id},
                                      {"$set": {"product_images": new_product_images}})
    return "image added"


# optional arg image_index; the method remove image by index. remove_all if no index
def remove_product_image(product_id: int, image_index: int = None):
    old_product_images = get_one_product(product_id)["product_images"]
    if image_index is None:
        new_product_images = []
        product_collection.update_one({"_id": product_id},
                                      {"$set": {"product_images": new_product_images}})
    else:
        new_product_images = old_product_images.remove(image_index)
        product_collection.update_one({"_id": product_id},
                                      {"$set": {"product_images": new_product_images}})
    return "image removed"


def update_product_description(product_id: int, product_description: str):
    product_collection.update_one({"_id": product_id}, {"$set": {"product_description": product_description}})
    return "description update successful"


def get_one_product(product_id: int):
    return product_collection.find_one({"_id": product_id})


def get_all_products():
    return [product for product in product_collection.find({})]
# ------------ product_collection methods end --------------------


# ------------ Private method --------------------
def __get_next_id_for(collection):
    id_object = collection.find_one({})
    if id_object:
        next_id = int(id_object["last_id"]) + 1
        collection.update_one({}, {"$set": {"last_id": next_id}})
        return next_id
    else:
        collection.insert_one({"last_id": 1})
        return 1

    
