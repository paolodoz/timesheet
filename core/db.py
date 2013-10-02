try:
    from pymongo import MongoClient as Connection
except ImportError as e:
    from pymongo import Connection

from validation import validate_criteria_projection, objectify_json_with_idstring, validate_transform_json_list, validate_transform_json, sanitize_json, stringify_objectid_list, stringify_json_list_with_objectid
from bson.objectid import ObjectId
from config import collections, conf_mongodb, conf_auth, conf_auth_db
import string, hashlib, random

connection = Connection(conf_mongodb['hostname'], conf_mongodb['port'])
db = connection[conf_mongodb['db']]

def get(collection, criteria_projection):
    """Get selected records from collection, and return it as json
    Called by GET /<collection>/"""
    
    criteria, projection = validate_criteria_projection(criteria_projection)
    
    criteria = objectify_json_with_idstring(criteria)
    return stringify_json_list_with_objectid(db[collection].find(sanitize_json(criteria), projection))


def remove(collection, criterias = []):
    """Remove selected records from collection
    Called by POST /remove/<collection>"""
    
    for criteria in criterias:
        
        criteria = objectify_json_with_idstring(criteria)
        
        db[collection].remove(sanitize_json(criteria))
            

def add(collection, documents_list):
    """Insert new record list to collection
    Called by POST /add/<collection>/"""
        
    return stringify_objectid_list(db[collection].insert(validate_transform_json_list(collection, documents_list)))

def update(collection, document):
    """Update an inserted record
    Called by POST /update/<collection>/"""
    
    document = objectify_json_with_idstring(validate_transform_json(collection, document))
    
    db[collection].update({ '_id' : document['_id'] }, document)
    