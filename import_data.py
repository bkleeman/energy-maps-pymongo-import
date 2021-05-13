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
            "start_date": 2012,
            "end_date": 2020
        }
    }
        
    pprint(json.dumps(props_str))
    file_data.update(props_str)
    pprint(file_data)

# append props to each file in the directory and insert each into the collection
def import_files():
    for filename in os.listdir('./'):
        if filename != 'import_data.py':
            with open(filename) as file:
                file_data = json.load(file)
                append_props_obj(file_data)

                if isinstance(file_data, list):
                    Collection.insert_many(file_data)
                else: Collection.insert_one(file_data)

import_files()

# We want to use create index

# declare schema for all records as a python object -- check line 160 of atlas_db ingestors mongodb.py file
# See the init file for where the AtlasSchema class is defined

# class AtlasMongoDocument(AtlasSchema):
#     def __init__(self, *args, **kwargs):
#         """Schema for storing ATLAS data in Mongo.
#         """
#         super(AtlasMongoDocument, self).__init__(*args, **kwargs)

#     @property
#     def __geo_interface__(self):
#         """Define centroid (x, y) as a GeoJSON point. n-d array of values
#          in the `properties` attribute.
#         :return: GeoJSON object representing data point
#         :rtype: dict
#         """

#         document = {
#             # 'type': 'Feature',
#             'geometry': {'type': 'Point',
#                          'coordinates': [self.x, self.y]},
#             'properties': {
#                 'values': self.value,
#             }}

#         return document