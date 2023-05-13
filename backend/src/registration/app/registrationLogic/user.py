import random
import pymongo
import os

def register(login, password):
    user_id = generate_id(login, password)
    user = { "login": login, "password": password, "_id": user_id }
    users_table = connect_to_mongodb("users")
    users_table.insert_one(user)
    return user_id

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

    