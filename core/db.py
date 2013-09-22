try:
    from pymongo import MongoClient as Connection
except ImportError, e:
    from pymongo import Connection

from core.validation import validate, sanitize_json
from core.config import collections

connection = Connection('localhost', 27017)
db = connection.ts

# Create on database missing collections names
for missing_collection in (set(collections) - set(db.collection_names())):
    db[missing_collection]

# Get selected records from collection
# Called by GET /<document>/
def get(collection, selection = {}):
    return db[collection].find(sanitize_json(selection))

# Remove selected records from collection
# Called by POST /del/<collection>
def remove(collection, selection = {}):
    return db[collection].remove(sanitize_json(selection))

# Insert new record to collection
# Called by POST /add/<collection>/
def add(collection, json):
    db[collection].insert(validate(collection, json))
    