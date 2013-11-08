try:
    from pymongo import MongoClient as Connection
except ImportError as e:
    from pymongo import Connection

from core.validation.validation import TSValidationError, validate_request, recursive_merge, update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from core.validation.permissions import check_get_permissions, check_upsert_permissions, check_remove_permissions
from bson.objectid import ObjectId
from core.config import collections, conf_mongodb, conf_auth, conf_auth_db
import string, hashlib, random, types, cherrypy, logging

connection = Connection(conf_mongodb['hostname'], conf_mongodb['port'])
db = connection[conf_mongodb['db']]

db_log_severity = logging.INFO

def get(collection, criteria_projection_order):
    """Get selected records from collection, and return it as json
    Called by GET /<collection>/"""
      
    # Check request format
    validate_request('get', criteria_projection_order)
      
    # Check permissions  
    check_get_permissions(collection, criteria_projection_order[0], criteria_projection_order[1], criteria_projection_order[2])
    
    # Sanify criteria (to match with sanified documents)
    sanified_criteria = sanitize_objectify_json(criteria_projection_order[0])
    
    cherrypy.log('%s' % (criteria_projection_order), context = 'TS.GET.%s.criteria_projection_order' % collection, severity = db_log_severity)
    
    # Request
    return stringify_objectid_cursor(db[collection].find( { '$query' : sanified_criteria, '$orderby' : criteria_projection_order[2] }, criteria_projection_order[1]))


def remove(collection, criterias = []):
    """Remove selected records from collection
    Called by POST /remove/<collection>"""

    # Check request format
    validate_request('remove', criterias)
    
    # Check permissions before requests  
    for criteria in criterias:
        check_remove_permissions(collection, criteria)

    # Sanify criteria (to match with sanified documents)
    sanified_criterias = sanitize_objectify_json(criterias)
    
    cherrypy.log('%s' % (criterias), context = 'TS.REMOVE.%s.criteria' % collection, severity = db_log_severity)
    
    # Requests
    for criteria in sanified_criterias:
        db[collection].remove(criteria)
            
def add(collection, documents_list):
    """Insert new record list to collection
    Called by POST /add/<collection>/"""

    # Check request format
    validate_request('add', documents_list)
    
    validate_json_list(collection, documents_list)

    for document in documents_list:
        check_upsert_permissions('add', collection, document)

    # Sanify documents
    sanified_documents_list = sanitize_objectify_json(documents_list)

    # Eventually rewrite password and salt
    update_password_salt_user_list(collection, sanified_documents_list)
    
    cherrypy.log('%s' % (sanified_documents_list), context = 'TS.ADD.%s.documents' % collection, severity = db_log_severity)
    
    # Request
    return stringify_objectid_list(db[collection].insert(sanified_documents_list))

def update(collection, document):
    """Update an inserted record
    Called by POST /update/<collection>/"""
    
    # Check request format
    validate_request('update', document)
        
    validate_json_list(collection, [ document ])
    check_upsert_permissions('update', collection, document)
    sanified_document = sanitize_objectify_json(document)
    
    cherrypy.log('%s' % (sanified_document), context = 'TS.UPDATE.%s.document' % collection, severity = db_log_severity)
    
    db_collection = db[collection].find_one({ '_id' : sanified_document['_id'] })
    db[collection].update({ '_id' : sanified_document['_id'] }, recursive_merge(db_collection, sanified_document))
    