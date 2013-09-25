try:
    from pymongo import MongoClient as Connection
except ImportError, e:
    from pymongo import Connection

from core.validation import objectify_json_with_idstring, validate_transform_json_list, validate_transform_json, sanitize_json, stringify_objectid_list, stringify_json_list_with_objectid
from bson.objectid import ObjectId
from core.config import collections, conf_mongodb, conf_auth, conf_auth_db
import string, hashlib, random

connection = Connection(conf_mongodb['hostname'], conf_mongodb['port'])
db = connection[conf_mongodb['db']]

def get(collection, selection = {}):
    """Get selected records from collection, and return it as json
    Called by GET /<collection>/"""
    
    selection = objectify_json_with_idstring(selection)
    
    return stringify_json_list_with_objectid(db[collection].find(sanitize_json(selection)))


def remove(collection, selections = []):
    """Remove selected records from collection
    Called by POST /remove/<collection>"""
    
    for selection in selections:
        
        selection = objectify_json_with_idstring(selection)
        
        db[collection].remove(sanitize_json(selection))
            

def add(collection, elements_list):
    """Insert new record list to collection
    Called by POST /add/<collection>/"""
        
    return stringify_objectid_list(db[collection].insert(validate_transform_json_list(collection, elements_list)))

def update(collection, element):
    """Update an inserted record
    Called by POST /update/<collection>/"""
    
    validated_element = objectify_json_with_idstring(validate_transform_json(collection, element))
    
    db[collection].update({ '_id' : validated_element['_id'] }, validated_element)
    