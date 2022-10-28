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

# Order(order_id: int, user_id: int, product_id_list: list[int])
# primary_key -> order_id, foreign_key -> user_id
order_collection = db["order"]

# Shopping_cart(cart_id: int, user_id: int, product_id_list: list[int])
# primary_key -> cart_id, foreign_key -> user_id
shopping_cart_collection = db["shopping_cart"]


# ------------ user_collection methods --------------------

def get_next_user_id():
    __get_next_id_for(user_id_collection)


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
        return "password reset successfully"
    else:
        return "password mismatching"


def get_one_user(user_id: int):
    return user_collection.find_one({"_id": user_id})


def get_all_users():
    return [user for user in user_collection.find({})]

# ------------ user_collection methods end --------------------

# ------------ product_collection methods --------------------


def get_next_product_id():
    __get_next_id_for(product_id_collection)













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
