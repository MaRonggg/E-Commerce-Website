from flask_pymongo import MongoClient

mongo_client = MongoClient('mongo')
db = mongo_client['5bytes']

# User_accounts(
#     user_id: int, password: str, email: str, name: str,
#     address1: str, address2: str, city: str, state: str, zip: str,
#     on_sale: list[int], order: list[int], cart: list[int]
# )
user_collection = db["User_account"]

# store the last id
user_id_collection = db["user_id"]

# Product (
#     product_id: int, product_name: str, product_price: double,
#     product_images: list[Path], product_description: str
# )
product_collection = db["product"]

# Sale(user_id: int, product_id_list: list[int])
# primary_key -> user_id
# sale_collection = db["sale"]


# Order(user_id: int, product_id_list: list[int])
# primary_key -> user_id
order_collection = db["order"]

# Shopping_cart(user_id: int, product_id_list: list[int])
# primary_key -> user_id
shopping_cart_collection = db["shopping_cart"]


def get_next_user_id():
    id_object = user_id_collection.find_one({})
    if id_object:
        next_id = int(id_object["last_id"]) + 1
        user_id_collection.update_one({}, {"$set": {"last_id": next_id}})
        return next_id
    else:
        user_id_collection.insert_one({"last_id": 1})
        return 1


def create_user_account(user_id: int, email: str, password: str, name: str):
    user_dict = {
        "_id": user_id,
        "email": email,
        "password": password,
        "name": name,
        "address1": "", "address2": "", "city": "", "state": "", "zip_code": ""
    }
    insert_result = user_collection.insert_one(user_dict)
    # print(insert_result.inserted_id)
    return get_one_user(insert_result.inserted_id)
#     address1: str, address2: str, city: str, state: str, zip: str


def update_user_address(user_id: int, password: str, address1: str, address2: str, city: str, state: str, zip_code: str):
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
