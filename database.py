import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
CONNECT_URL = os.getenv("CONNECT_URL")


cluster = MongoClient(CONNECT_URL)
'''
db = cluster.ctox
serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)
'''
db = cluster["valdb"]
collection = db["userbytag"] 

def set_record(id,name,tag,details):
    if collection.count_documents({"_id": id}, limit=1) == 0:
        collection.insert_one({"_id": id, "display_name": name,"tag": tag,"details": details})
    else:
        collection.update_one({"_id": id}, {"$set": {"display_name": name,"details": details}})

def get_record(id):
    query={"_id": id}
    try:
        collection.find_one(query)
    except:
        return "member not linked"




