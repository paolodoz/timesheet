try:
    from pymongo import MongoClient as Connection
except ImportError, e:
    from pymongo import Connection

from bson import json_util
from core.validation import validate, sanitize_json
from core.config import collections
import json


connection = Connection('localhost', 27017)
db = connection.ts

# Create on database missing collections names
for missing_collection in (set(collections) - set(db.collection_names())):
    db[missing_collection]

# Get selected records from collection, and return it as json
# Called by GET /<document>/
def get(collection, selection = {}):
    cursors = db[collection].find(sanitize_json(selection))
    json_out = []
    for cursor in cursors:
        del cursor['_id']
        json_out.append(cursor)
    return json_out


# Remove selected records from collection
# Called by POST /remove/<collection>
def remove(collection, selection = {}):
    db[collection].remove(sanitize_json(selection))

# Insert new record to collection
# Called by POST /add/<collection>/
def add(collection, json):
    db[collection].insert(validate(collection, json))
    