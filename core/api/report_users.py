from core.validation.validation import TSValidationError, validate_request, update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from core.validation.permissions import check_datamine_permissions
from core.config import conf_reports, conf_approved
from bson.objectid import ObjectId
from core.api.crud import db
import cherrypy, logging


def report_users_hours(criteria):
    
    """
    Get report grouped by users
    
    POST /data/report_users_hours/
    
    Expects a  { 'start' : '', 'end' : '', 'users' : [], 'projects' : [], hours_standard : bool, hours_extra : bool, tasks : [] } 
    Returns { 'error' : string, 'records' : [ { }, { }, .. ]  } 
    """
    
    validate_request('report_users_hours', criteria)
    sanified_criteria = sanitize_objectify_json(criteria)
    
    
    # Prepare the aggregation pipe
    
    dates_match = { "date": { 
                           '$lte' : sanified_criteria['end'], 
                           '$gte' : sanified_criteria['start'] 
                           }
                 }
    
    
    match_users_projects_extras_tasks = { }
    # Match optional users
    if sanified_criteria['users_ids']:
        match_users_projects_extras_tasks['users.user_id'] = { '$in' : sanified_criteria['users_ids'] } 
    
    # Match optional projects filters
    if sanified_criteria['projects']:
        match_users_projects_extras_tasks['users.hours.project'] = { '$in' : sanified_criteria['projects'] }
    
    # Match optional extra hours filter 
    if sanified_criteria['hours_standard'] == True and sanified_criteria['hours_extra'] == False:
        match_users_projects_extras_tasks['users.hours.isextra'] = False
    elif sanified_criteria['hours_standard'] == False and sanified_criteria['hours_extra'] == True:
        match_users_projects_extras_tasks['users.hours.isextra'] = True
        
    # Match optional task filter
    if sanified_criteria['tasks']:
        match_users_projects_extras_tasks['users.hours.task'] = { '$in' : sanified_criteria['tasks'] }
    
    check_datamine_permissions('report_users_hours', match_users_projects_extras_tasks)
    
    aggregation_pipe = [ 
                        { '$match': dates_match },
                        { '$unwind' : '$users' }, 
                        { '$unwind' : '$users.hours' }, 
                        { '$match' : match_users_projects_extras_tasks },
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
    
    
    