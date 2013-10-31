from core.validation.validation import TSValidationError, validate_request, update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from core.validation.permissions import check_action_permissions, check_criteria_permissions, check_projection_permissions, check_insert_permissions
from bson.objectid import ObjectId
from core.api.crud import db
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

        check_insert_permissions('push_days', sanified_document)

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
    check_criteria_permissions('search_days', prepared_criteria)
    
    # Prepare the projection to return only date and users.date where user id is correct
    projection = { 'date' : 1, 'users' : { '$elemMatch' : { 'user_id' : user_id }}}

    return { 'records' : stringify_objectid_cursor(db.day.find(prepared_criteria, projection)) }


def report_users_hours(criteria):
    
    """
    Get report grouped by users
    
    POST /data/report_users_hours/
    
    Expects a  { 'start' : '', 'end' : '', 'users' : [], 'projects' : [], hours_standard : bool, hours_extra : bool, tasks : [] } 
    Returns { 'error' : string, 'records' : [ { }, { }, .. ]  } 
    """
    
    check_action_permissions('report_users_hours', 'report_users_hours')
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
    
    check_criteria_permissions('report_users_hours', match_users_projects_extras_tasks)
    
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
    
    
    

def report_projects(criteria):
    
    """
    Get projects report
    
    POST /data/report_projects/
    
    Expects { 'start' : '', 'end' : '', 'customer' : '', 'projects' : [] } 
    Returns { 'error' : string, 'records' : [ [ 'YYYY-MM', 2 ], [ 'YYYY-MM', 4 ], .. ]  } 
    """
    
    
    def _find_days_from_customers(sanified_criteria):
            
        # Get projects by customer
        customer_input = sanified_criteria.get('customer')
        if customer_input:
            projects_input = []
            customer_projects = db.project.find( { 'customer' : customer_input }, { '_id' : 1 })
            for project in customer_projects:
                projects_input.append(str(project['_id'])) 
        else:
            projects_input = sanified_criteria.get('projects', [])
        
        # Prepare the aggregation pipe
        
        dates_match = { "date": { 
                               '$lte' : sanified_criteria['end'], 
                               '$gte' : sanified_criteria['start'] 
                               }
                     }
        
        match_projects = { }
        
        # Match optional projects filters
        if projects_input:
            match_projects['users.hours.project'] = { '$in' : projects_input }
        
        check_criteria_permissions('report_projects', match_projects)
        
        aggregation_pipe = [ 
                            { '$match': dates_match },
                            { '$unwind' : '$users' }, 
                            { '$unwind' : '$users.hours' }, 
                            { '$match' : match_projects },
                             { '$group' : 
                              { '_id' : { 
                                         'user_id' : '$users.user_id', 
                                         'date' : '$date' 
                                         }, 
                               'hours' : { '$sum' : '$users.hours.amount'  } 
                               } 
                              } 
                            ]
                           
        cherrypy.log(aggregation_pipe.__repr__(), context = 'TS.REPORT_PROJECTS.days_aggregation', severity = logging.INFO)
        
        return db.day.aggregate(aggregation_pipe)

    def _find_salaries_from_date_users(days_ids_list, end, start):
        # TODO: misure if _id filter now is superflous due to filter check during merge
        aggregation_pipe = [ { '$match' : { 'salary.cost' : { '$gt' : 0 }, '_id' : { '$in' : days_ids_list } } }, { '$project' : { 'salary.from' : 1, 'salary.to' : 1, 'salary.cost' : 1, '_id' : 1 } } ]
        cherrypy.log(aggregation_pipe.__repr__(), context = 'TS.REPORT_PROJECTS.salaries_aggregation', severity = logging.INFO)
        return db.user.aggregate(aggregation_pipe)


    check_action_permissions('report_projects', 'report_projects')
    validate_request('report_projects', criteria)
    sanified_criteria = sanitize_objectify_json(criteria)
        
    
    # Day mining
    days_result = _find_days_from_customers(sanified_criteria)['result'] 
    days_ids_list = [ ObjectId(r['_id']['user_id']) for r in days_result ]
    
    # Salary mining
    salaries_result = _find_salaries_from_date_users(days_ids_list, sanified_criteria['end'], sanified_criteria['start'])['result']
    users_ids_list = [ r['_id'] for r in salaries_result ]

    ### MERGE
    costs_dict = {}
    for day in days_result:
        
        user_record = day.get('_id',{})
        user_id = user_record.get('user_id')
        user_date = user_record.get('date')
        user_YM = '-'.join(user_date.split('-')[:2])
        user_hours = day.get('hours', 0)

        cost = next((sal['salary'][0]['cost'] for sal in salaries_result if sal['_id'] == ObjectId(user_id) and sal['salary'][0]['from'] <= user_date and sal['salary'][0]['to'] >= user_date ), 0)
        
        if cost:
            costs_dict[user_YM] = costs_dict.get(user_YM, 0)  + ( cost * user_hours )
             
    ## ORDER
    costs_list = []
    for ym in sorted(costs_dict.keys()):
        costs_list.append( (ym, costs_dict[ym]) )
                
    return { 'records' : stringify_objectid_cursor(costs_list) }
    