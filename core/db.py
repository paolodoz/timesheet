try:
    from pymongo import MongoClient as Connection
except ImportError as e:
    from pymongo import Connection

from validation import validate_criteria_projection, objectify_json_with_idstring, validate_transform_json_list, validate_transform_json, sanitize_json, stringify_objectid_list, stringify_json_list_with_objectid
from permissions import restrict_criteria, deny_requests
from bson.objectid import ObjectId
from config import collections, conf_mongodb, conf_auth, conf_auth_db
import string, hashlib, random

connection = Connection(conf_mongodb['hostname'], conf_mongodb['port'])
db = connection[conf_mongodb['db']]

def get(collection, criteria_projection):
    """Get selected records from collection, and return it as json
    Called by GET /<collection>/"""
    
    criteria, projection = validate_criteria_projection(criteria_projection)
    
    deny_requests('get', collection, projection)
    
    restricted_criteria = restrict_criteria('get', collection, criteria)
    objectified_criteria = objectify_json_with_idstring(restricted_criteria)
    sanified_criteria = sanitize_json(criteria)
    
    return stringify_json_list_with_objectid(db[collection].find(sanified_criteria, projection))


def remove(collection, criterias = []):
    """Remove selected records from collection
    Called by POST /remove/<collection>"""
    
    for criteria in criterias:
        
        deny_requests('remove', collection)
        
        objectified_criteria = objectify_json_with_idstring(criteria)
        db[collection].remove(sanitize_json(objectified_criteria))
            

def add(collection, documents_list):
    """Insert new record list to collection
    Called by POST /add/<collection>/"""
    
    deny_requests('add', collection)
    
    validated_json = validate_transform_json_list(collection, documents_list)
    return stringify_objectid_list(db[collection].insert(validated_json))

def update(collection, document):
    """Update an inserted record
    Called by POST /update/<collection>/"""
    
    deny_requests('update', collection)
    objectified_document = objectify_json_with_idstring(validate_transform_json(collection, document))
    
    db[collection].update({ '_id' : objectified_document['_id'] }, objectified_document)
    