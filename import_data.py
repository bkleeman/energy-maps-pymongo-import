import json
from pprint import pprint
from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:27017/")

db = client["pymongo_test"]

Collection = db["data"]

# Add a props entry to the end of each record with a start/end date to function as
# a mongo index to filter by year for our database calls
def append_props_obj(file_data):
    props_str = {
        "props": {
            "start date": 2012,
            "end date": 2020
        }
    }
        
    pprint(json.dumps(props_str))
    file_data.update(props_str)
    pprint(file_data)

# append props to each file in the directory and insert each into the collection
def import_files():
    for filename in os.listdir('./'):
        with open(filename) as file:
            file_data = json.load(file)
            append_props_obj(file_data)

            if isinstance(file_data, list):
                Collection.insert_many(file_data)
            else: Collection.insert_one(file_data)

import_files()