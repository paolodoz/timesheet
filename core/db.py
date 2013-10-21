try:
    from pymongo import MongoClient as Connection
except ImportError as e:
    from pymongo import Connection

from validation import TSValidationError, recursive_merge, update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from permissions import check_action_permissions, check_criteria_permissions, check_projection_permissions
from bson.objectid import ObjectId
from config import collections, conf_mongodb, conf_auth, conf_auth_db
import string, hashlib, random, types, cherrypy, logging

connection = Connection(conf_mongodb['hostname'], conf_mongodb['port'])
db = connection[conf_mongodb['db']]

db_log_severity = logging.INFO

def get(collection, criteria_projection):
    """Get selected records from collection, and return it as json
    Called by GET /<collection>/"""
    
    if (isinstance(criteria_projection, types.ListType) and len(criteria_projection) == 2 and criteria_projection[1]):
        criteria, projection = criteria_projection
    else:
        raise TSValidationError('Expected list with criteria and nonempty projection')
      
    # Check permissions  
    check_action_permissions('get', collection)
    check_criteria_permissions(collection, criteria)
    check_projection_permissions(collection, projection)
    
    # Sanify criteria (to match with sanified documents)
    sanified_criteria = sanitize_objectify_json(criteria)
    
    cherrypy.log('%s' % (sanified_criteria), context = 'TS.GET.%s.criteria' % collection, severity = db_log_severity)
    cherrypy.log('%s' % (projection), context = 'TS.GET.%s.projection' % collection, severity = db_log_severity)
    
    # Request
    return stringify_objectid_cursor(db[collection].find(sanified_criteria, projection))


def remove(collection, criterias = []):
    """Remove selected records from collection
    Called by POST /remove/<collection>"""
    
    # Check permissions before requests  
    check_action_permissions('remove', collection)
    for criteria in criterias:
        check_criteria_permissions(collection, criteria)

    # Sanify criteria (to match with sanified documents)
    sanified_criterias = sanitize_objectify_json(criterias)
    
    cherrypy.log('%s' % (criterias), context = 'TS.REMOVE.%s.criteria' % collection, severity = db_log_severity)
    
    # Requests
    for criteria in sanified_criterias:
        db[collection].remove(criteria)
            
def add(collection, documents_list):
    """Insert new record list to collection
    Called by POST /add/<collection>/"""
    
    
    # Check permission
    if not isinstance(documents_list, list):
        raise TSValidationError("List expected, not '%s'" % documents_list.__class__.__name__)
    check_action_permissions('add', collection)
    validate_json_list(collection, documents_list)
    
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
    
    # Check permission
    if not (isinstance(document, types.DictType) and  '_id' in document):
        raise TSValidationError("Dict with '_id' field expected, not '%s'" % document.__class__.__name__)
    
    check_action_permissions('update', collection)
    check_criteria_permissions(collection, document)
    
    # Sanify documents
    sanified_document = sanitize_objectify_json(document)
    
    cherrypy.log('%s' % (document), context = 'TS.UPDATE.%s.document' % collection, severity = db_log_severity)
    
    db_collection = db[collection].find_one({ '_id' : sanified_document['_id'] })
    db[collection].update({ '_id' : sanified_document['_id'] }, recursive_merge(db_collection, sanified_document))
    