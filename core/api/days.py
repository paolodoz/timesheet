from core.validation.permissions import check_datamine_permissions
from core.validation.validation import TSValidationError, validate_request, update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from bson.objectid import ObjectId
from core.api.crud import db
import cherrypy, logging


def push_days(documents_list):
    
    """
    Add or update new hours in day collection
    
    POST /data/push_days/
    
    Expects a list of 'day' elements. Push only one user per day.
    Returns { 'error' : string }
    """
    
    validate_request('push_days', documents_list)
    validate_json_list('day', documents_list)
    for document in documents_list:
        check_datamine_permissions('push_days', document)

    sanified_documents_list = sanitize_objectify_json(documents_list)
    
    for sanified_document in sanified_documents_list:

        date = sanified_document['date']
        
        found = db.day.find({ 'date' : date }).limit(1).count()

        users = sanified_document.get('users', [])

        # Validate one user per day insertion
        if len(users) > 1:
            raise TSValidationError("Push only one user per day")

        # If the date is already present and an user is specified
        if found and users:
                                     
            user_id = users[0]['user_id']
            
            # Drop old user data
            db.day.update({'date': date }, {'$pull': {'users': {'user_id': user_id }}})
            # Push new one
            db.day.update({'date': date }, {'$push': {'users': {'user_id': user_id, 'hours' : users[0]['hours'] }}})
        
        # If the data does not already exist and there are new users data, insert it
        elif not found and users:
            db.day.insert(sanified_document)
            
        # If there is already the date but no new user data, skip it
        else:
            pass

    return { }

def search_days(criteria):
    
    """
    Get day by collection
    
    POST /data/search_days/    
    
    Expects a  { 'start' : 'date1', 'end' : 'date2', 'user_id' : 'user_id' } 
    Returns { 'error' : string, 'records' : [ { }, { }, .. ]  } 
    """
    
    validate_request('search_days', criteria)
    
    sanified_criteria = sanitize_objectify_json(criteria)

    user_id = sanified_criteria['user_id']

    # Prepare the criteria with date range && user_id
    prepared_criteria = { "date" :  {"$gte": sanified_criteria['start'], "$lte": sanified_criteria['end']}, "users.user_id" : user_id }
    check_datamine_permissions('search_days', prepared_criteria)
    
    # Prepare the projection to return only date and users.date where user id is correct
    projection = { 'date' : 1, 'users' : { '$elemMatch' : { 'user_id' : user_id }}}

    cherrypy.log('%s\n%s' % (prepared_criteria, projection), context = 'TS.SEARCH_DAYS.criteria_projection', severity = logging.INFO)
    
    return { 'records' : stringify_objectid_cursor(db.day.find(prepared_criteria, projection)) }

