try:
    from pymongo import MongoClient as Connection
except ImportError as e:
    from pymongo import Connection

from validation import recursive_merge, update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from permissions import restrict_criteria, check_request_permissions
from bson.objectid import ObjectId
from config import collections, conf_mongodb, conf_auth, conf_auth_db
import string, hashlib, random
from validictory import ValidationError

connection = Connection(conf_mongodb['hostname'], conf_mongodb['port'])
db = connection[conf_mongodb['db']]

def get(collection, criteria_projection):
    """Get selected records from collection, and return it as json
    Called by GET /<collection>/"""
    
    if (isinstance(criteria_projection, list) and len(criteria_projection) == 2 and criteria_projection[1]):
        criteria, projection = criteria_projection
    else:
        raise ValidationError('Expected list with criteria and nonempty projection')
        
    check_request_permissions('get', collection, projection)
    restricted_criteria = restrict_criteria('get', collection, criteria)
    
    sanified_criteria = sanitize_objectify_json(criteria)
    print '[TS_DEBUG_CRITERIA] %s' % (sanified_criteria)
    return stringify_objectid_cursor(db[collection].find(sanified_criteria, projection))


def remove(collection, criterias = []):
    """Remove selected records from collection
    Called by POST /remove/<collection>"""
    
    check_request_permissions('remove', collection)
    criterias = sanitize_objectify_json(criterias)
    for criteria in criterias:
        db[collection].remove(criteria)
            
def add(collection, documents_list):
    """Insert new record list to collection
    Called by POST /add/<collection>/"""
    
    if not isinstance(documents_list, list):
        raise ValidationError("List expected, not '%s'" % documents_list.__class__.__name__)
    
    check_request_permissions('add', collection)
    validate_json_list(collection, documents_list)
    
    sanified_documents_list = sanitize_objectify_json(documents_list)
    update_password_salt_user_list(collection, sanified_documents_list)
    
    return stringify_objectid_list(db[collection].insert(sanified_documents_list))

def update(collection, document):
    """Update an inserted record
    Called by POST /update/<collection>/"""
    
    check_request_permissions('update', collection)
    sanified_document = sanitize_objectify_json(document)
    
    db_collection = db[collection].find_one({ '_id' : sanified_document['_id'] })
    db[collection].update({ '_id' : sanified_document['_id'] }, recursive_merge(db_collection, sanified_document))
    