from validation import update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from permissions import restrict_criteria, check_request_permissions
from bson.objectid import ObjectId
from validictory import ValidationError
from core.db import db

def push_days(documents_list):
    
    """
    Add or update new hours in day collection
    
    POST /data/push_days/
    
    Expects a list of 'day' collections. Push only one user per day.
    Returns { 'error' : string }
    """
    
    check_request_permissions('update', 'day')
    validate_json_list('day', documents_list)
    
    sanified_documents_list = sanitize_objectify_json(documents_list)
    
    for sanified_document in sanified_documents_list:

        date = sanified_document['date']
        
        found = db.day.find({ 'date' : date }).limit(1).count()

        if found and sanified_document.get('users') and 'user_id' in sanified_document['users'][0]:
                         
            # Validate one user per day insertion
            if len(sanified_document['users']) > 1:
                raise ValidationError("Push only one user per day")
            
            user_id = sanified_document['users'][0]['user_id']
            
            db.day.update({'date': date }, {'$pull': {'users': {'user_id': user_id }}})
            db.day.update({'date': date }, {'$push': {'users': {'user_id': user_id, 'hours' : sanified_document['users'][0]['hours'] }}})
        else:
            db.day.insert(sanified_document)

    return { }


def search_days(criteria):
    
    """
    Get day by collection
    
    POST /data/search_days/
    
    Expects a  { 'date_from' : 'date1', 'date_to' : 'date2', 'user_id' : 'user_id' } 
    
    Returns { 'error' : string, 'records' : [ { }, { }, .. ]  } 
    """
    
    # TODO: Validate with validictory. Test also values.
    if not (sorted(criteria.keys()) == sorted(('date_from', 'date_to', 'user_id'))):
        raise ValidationError("Expected list with 'date_from', 'date_to', 'user_id' keys")
    
    # TODO: restrict user_id search with permissions  
        
    sanified_criteria = sanitize_objectify_json(criteria)

    user_id = sanified_criteria['user_id']

    # Prepare the criteria with date range && user_id
    criteria_range_user = { "date" :  {"$gte": sanified_criteria['date_from'], "$lte": sanified_criteria['date_to']}, "users.user_id" : user_id }
    
    # Prepare the projection to return only date and users.date where user id is correct
    projection = { 'date' : 1, 'users' : { '$elemMatch' : { 'user_id' : user_id }}}

    return { 'records' : stringify_objectid_cursor(db.day.find(criteria_range_user, projection)) }
    