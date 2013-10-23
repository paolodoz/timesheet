from validation import validate_data_request, update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from permissions import check_action_permissions, check_criteria_permissions, check_projection_permissions, check_insert_permissions
from bson.objectid import ObjectId
from core.validation import TSValidationError
from core.db import db
import cherrypy, logging

try:
    from pymongo.objectid import ObjectId
except ImportError as e:
    from bson import ObjectId

def push_days(documents_list):
    
    """
    Add or update new hours in day collection
    
    POST /data/push_days/
    
    Expects a list of 'day' collections. Push only one user per day.
    Returns { 'error' : string }
    """
    
    validate_json_list('day', documents_list)
    
    sanified_documents_list = sanitize_objectify_json(documents_list)
    
    for sanified_document in sanified_documents_list:

        check_insert_permissions('day', sanified_document)

        date = sanified_document['date']
        
        found = db.day.find({ 'date' : date }).limit(1).count()

        users = sanified_document.get('users', [])

        # Validate one user per day insertion
        if len(users) > 1:
            raise TSValidationError("Push only one user per day")

        if found and users and 'user_id' in sanified_document['users'][0]:
                                     
            user_id = users[0]['user_id']
            
            db.day.update({'date': date }, {'$pull': {'users': {'user_id': user_id }}})
            db.day.update({'date': date }, {'$push': {'users': {'user_id': user_id, 'hours' : users[0]['hours'] }}})
        else:
            db.day.insert(sanified_document)

    return { }


def search_days(criteria):
    
    """
    Get day by collection
    
    POST /data/search_days/
    
    Expects a  { 'start' : 'date1', 'end' : 'date2', 'user_id' : 'user_id' } 
    Returns { 'error' : string, 'records' : [ { }, { }, .. ]  } 
    """
    
    validate_data_request('search_days', criteria)
    
    sanified_criteria = sanitize_objectify_json(criteria)

    user_id = sanified_criteria['user_id']

    # Prepare the criteria with date range && user_id
    prepared_criteria = { "date" :  {"$gte": sanified_criteria['start'], "$lte": sanified_criteria['end']}, "users.user_id" : user_id }
    check_criteria_permissions('day', prepared_criteria)
    
    # Prepare the projection to return only date and users.date where user id is correct
    projection = { 'date' : 1, 'users' : { '$elemMatch' : { 'user_id' : user_id }}}

    return { 'records' : stringify_objectid_cursor(db.day.find(prepared_criteria, projection)) }


def report_users_hours(criteria):
    
    """
    Get report grouped by users
    
    POST /data/search_days/
    
    Expects a  { 'start' : '', 'end' : '', 'users' : [], 'projects' : [], hours_standard : bool, hours_extra : bool, tasks : [] } 
    Returns { 'error' : string, 'records' : [ { }, { }, .. ]  } 
    """
    
    validate_data_request('report_users_hours', criteria)
    sanified_criteria = sanitize_objectify_json(criteria)
    
    
    # Prepare the aggregation pipe
    
    
    matches_on_users = {}
    if sanified_criteria['users_ids']:
        matches_on_users['users_ids'] = { '$in' : sanified_criteria['users_ids'] }
    
    matches_on_users_hours = { }
    # Match optional projects filters
    if sanified_criteria['projects']:
        matches_on_users_hours['users.hours.project'] = { '$in' : sanified_criteria['projects'] }
    
    # Match optional extra hours filter 
    if sanified_criteria['hours_standard'] == True and sanified_criteria['hours_extra'] == False:
        matches_on_users_hours['users.hours.isextra'] = True
    elif sanified_criteria['hours_standard'] == False and sanified_criteria['hours_extra'] == True:
        matches_on_users_hours['users.hours.isextra'] = False
        
    # Match optional task filter
    if sanified_criteria['tasks']:
        matches_on_users_hours['users.hours.task'] = { '$in' : sanified_criteria['tasks'] }
    
    aggregation_pipe = [ 
                        { '$match': 
                         { "date": 
                          { '$lte' : sanified_criteria['end'], 
                           '$gte' : sanified_criteria['start'] } 
                          } }, 
                        { '$unwind' : '$users' }, 
                        { '$match': matches_on_users 
                         }, 
                        { '$unwind' : '$users.hours' }, 
                        { '$match' : matches_on_users_hours
                         },
                         { '$group' : 
                          { '_id' : { 
                                     'user_id' : '$users.user_id', 
                                     'date' : '$date' 
                                     }, 
                           'hours' : { '$push' : '$users.hours'  } 
                           } 
                          }, 
                        { '$sort' : { '_id.user_id' : 1, '_id.date' : 1 } }
                        ]
                       
    cherrypy.log(aggregation_pipe.__repr__(), context = 'TS.REPORT_USER_HOURS.aggregation', severity = logging.INFO)
    
    aggregation_result = db.day.aggregate(aggregation_pipe)
    
    return { 'records' : stringify_objectid_cursor(aggregation_result['result']) }
    