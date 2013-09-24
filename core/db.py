try:
    from pymongo import MongoClient as Connection
except ImportError, e:
    from pymongo import Connection

from core.validation import objectify_json_with_idstring, validate_sanitize_json_list, sanitize_json, stringify_objectid_list, stringify_json_list_with_objectid
from bson.objectid import ObjectId
from core.config import collections, conf_mongodb, conf_auth, conf_auth_db
import string, hashlib, random

connection = Connection(conf_mongodb['hostname'], conf_mongodb['port'])
db = connection[conf_mongodb['db']]

private_collections = [ 'password' ]

# Get selected records from collection, and return it as json
# Called by GET /<collection>/
def get(collection, selection = {}):
    
    selection = objectify_json_with_idstring(selection)
    
    return stringify_json_list_with_objectid(db[collection].find(sanitize_json(selection)))

# Remove selected records from collection
# Called by POST /remove/<collection>
def remove(collection, selections = []):
    for selection in selections:
        
        selection = objectify_json_with_idstring(selection)
        
        db[collection].remove(sanitize_json(selection))
            
    
# Insert new record list to collection
# Called by POST /add/<collection>/
def add(collection, elements_list):
    return stringify_objectid_list(db[collection].insert(validate_sanitize_json_list(collection, elements_list)))

    