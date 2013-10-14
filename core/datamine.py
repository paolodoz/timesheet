from validation import update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from permissions import restrict_criteria, check_request_permissions
from bson.objectid import ObjectId
from validictory import ValidationError
from core.db import db

def push_days(documents_list):
    
    """
    Add or update new hours in day collection
    
    POST /data/push_days/
    
    Expects a list of 'day' collections. Assume that for every item in the list there is only
    a single date of a single user.
    Returns { 'error' : string }
    """
    
    check_request_permissions('update', 'day')
    validate_json_list('day', documents_list)
    
    sanified_documents_list = sanitize_objectify_json(documents_list)
    
    for sanified_document in sanified_documents_list:
        
        if len(sanified_document['users_hours']) > 1:
            raise ValidationError("Only one user for day is supported on push_day")
        
        user_id =  sanified_document['users_hours'].keys()[0]
        
        spec = { "$and": [ { "date" : sanified_document['date'] }, {'users_hours.%s' % (user_id) : { '$exists' : True } } ] }
        document = { "$set" : { 'date' : sanified_document['date'], 'users_hours.%s' % (user_id) : sanified_document['users_hours'][user_id] }}
        
        db['day'].update( spec, document, upsert=True )
        
    return { }


def search_days(criteria_projection):
    
    """
    Get day by collection
    
    POST /data/search_days/
    
    Expects a  [ { 'date_from' : 'date1', 'date_to' : 'date2', 'user_id' : 'user_id' }, { 'fk2' : 1 } ]
    
    Returns { 'error' : string, 'records' : [ { 'data' : '', 'fk2' : '' }, { .. }, .. ]  } 
    """
    
    if (isinstance(criteria_projection, list) and len(criteria_projection) == 2 and criteria_projection[1]):
        criteria, projection = criteria_projection
    else:
        raise ValidationError('Expected list with criteria and nonempty projection')
    
    # TODO: Validate with validictory. Test also values.
    if not (sorted(criteria.keys()) == sorted(('date_from', 'date_to', 'user_id'))):
        raise ValidationError("Expected list with 'date_from', 'date_to', 'user_id' keys")
        
    check_request_permissions('get', 'day', projection)
    restricted_criteria = restrict_criteria('get', 'day', criteria)
    sanified_criteria = sanitize_objectify_json(criteria)

    user_id = sanified_criteria['user_id']

    # Prepare the criteria with date range && user_id
    criteria_range_user = { "$and": [ { "date" :  {"$gte": sanified_criteria['date_from'], "$lte": sanified_criteria['date_to']} }, {'users_hours.%s' % (user_id) : { '$exists' : True } } ] }
    
    # Prepare the projection with date and user_hours.user_id.specified_keys
    projection_user_hours = { 'date' : 1 } 
    for projkey, projvalue in projection.items():
        projection_user_hours['users_hours.%s.%s' % (user_id, projkey)] = projvalue

    return { 'records' : stringify_objectid_cursor(db['day'].find(criteria_range_user, projection_user_hours)) }
    