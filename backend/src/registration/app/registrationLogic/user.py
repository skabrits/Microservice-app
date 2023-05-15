import random
import pymongo
import os

def register(login, password):
    user_id = generate_id(login, password)
    user = { "login": login, "password": password, "_id": user_id }
    users_table = connect_to_mongodb("users")
    if users_table.find_one({"login": login}) is None:
        users_table.insert_one(user)
    else:
        user_id = None
    return user_id
    
def login(login, password):
    users_table = connect_to_mongodb("users")
    user = users_table.find_one({"login" : login})
    if user["password"] == password:
        user_id = user["_id"]
    return user_id
    
def check_user(user_id):
    result = True
    users_table = connect_to_mongodb("users")
    user = users_table.find_one({"_id" : user_id})
    if user is None:
        result = False
    return result

def generate_id(login, password):
    random.seed(str(login+password))
    seed_part = random.randint(100000,1000000)
    random.seed()
    random_part = random.randint(100000,1000000)
    return str(seed_part)+str(random_part)

def connect_to_mongodb(table_name):
    connection_url = os.getenv('DB_URL')
    myclient = pymongo.MongoClient(connection_url)
    mydb = myclient["project"]
    return mydb[table_name]

    