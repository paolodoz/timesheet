from core.validation.validation import TSValidationError, validate_request, update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from core.validation.permissions import check_action_permissions, check_criteria_permissions, check_projection_permissions, check_insert_permissions
from bson.objectid import ObjectId
from core.api.crud import db
import cherrypy, logging

try:
    from pymongo.objectid import ObjectId
except ImportError as e:
    from bson import ObjectId



def push_expences(documents_list):
    
    """
    Add new expences in projects
    
    POST /data/push_expences/
    
    Expects a list of 'project' elements having the 'project.expences' subdocument.
    Returns the { 'error' : string, 'ids' : [] }
    """
    
    validate_json_list('project', documents_list)
    
    sanified_documents_list = sanitize_objectify_json(documents_list)
    
    expences_ids = []
    
    cherrypy.log(str(sanified_documents_list), context = 'TS.PUSH_EXPENCES', severity = logging.INFO)
    
    for sanified_document in sanified_documents_list:

        check_insert_permissions('push_expences', sanified_document)

        project_id = sanified_document['_id']

        found = db.project.find({ '_id' : project_id }).limit(1).count()

        # If found
        if found:
            for expence in sanified_document['expences']:
    
                 # Add just generated expence_id to the object             
                 expence_id = str(ObjectId())
                 
                 expence['_id'] = expence_id
                 
                 # Push new one
                 db.project.update({'_id': project_id }, {'$push' : { 'expences' : expence }})

                 expences_ids.append(expence_id)

    return { 'ids' : expences_ids }

def push_days(documents_list):
    
    """
    Add or update new hours in day collection
    
    POST /data/push_days/
    
    Expects a list of 'day' elements. Push only one user per day.
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
    
    Expects { 'start' : '', 'end' : '', 'customer' : '', 'projects' : [], 'mode' : 'total|project' } 
    Returns with mode total
       { 'error' : string, 'records' : [ [ 'YYYY-MM', 2 ], [ 'YYYY-MM', 4 ], .. ]  } 
    Returns with mode total
       { 'error' : string, 'records' : {  'proj1' : [ [ 'YYYY-MM', 2 ], [ 'YYYY-MM', 4 ] ], .. }  } 
    """
    
    def _find_project_list_by_customer(sanified_criteria):
        
        # Get projects by customer
        customer_input = sanified_criteria.get('customer')
        if customer_input:
            projects_input = []
            customer_projects = db.project.find( { 'customer' : customer_input }, { '_id' : 1 })
            for project in customer_projects:
                projects_input.append(str(project['_id'])) 
        else:
            projects_input = sanified_criteria.get('projects', [])
            
        return projects_input
    
    def _find_days_by_projects(projects_input, sanified_criteria):
            
        
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
                                         'date' : '$date',
                                         'project' : '$users.hours.project'
                                         }, 
                               'hours' : { '$sum' : '$users.hours.amount'  } 
                               } 
                              } 
                            ]
                           
        cherrypy.log(aggregation_pipe.__repr__(), context = 'TS.REPORT_PROJECTS.days_aggregation', severity = logging.INFO)
        
        return db.day.aggregate(aggregation_pipe)

    def _find_salaries_by_date_users(days_ids_list, end, start):
        # TODO: misure if _id filter now is superflous due to filter check during merge
        aggregation_pipe = [ { '$match' : { 'salary.cost' : { '$gt' : 0 }, '_id' : { '$in' : days_ids_list } } }, { '$project' : { 'salary.from' : 1, 'salary.to' : 1, 'salary.cost' : 1, '_id' : 1 } } ]
        cherrypy.log(aggregation_pipe.__repr__(), context = 'TS.REPORT_PROJECTS.salaries_aggregation', severity = logging.INFO)
        return db.user.aggregate(aggregation_pipe)

    def _find_costs_by_project_date(projects_input, end, start):

        objectified_projects_input = [ ObjectId(p) for p in projects_input ]

        if projects_input:
            match_projects = { '_id' : { '$in' : objectified_projects_input }  }
        else:
            match_projects = {}

        aggregation_pipe = [ { '$match' : match_projects }, { '$unwind' : '$economics'}, { '$match' : { 'economics.period' : { '$gte' : start, '$lte' : end } } }, { '$group' : { '_id' : { 'project_id' : '$_id', 'period' : '$economics.period', 'budget' : '$economics.budget', 'extra' : '$economics.extra'   } } } ]
        cherrypy.log(aggregation_pipe.__repr__(), context = 'TS.REPORT_PROJECTS.projects_aggregation', severity = logging.INFO)
        return db.project.aggregate(aggregation_pipe)

    def _merge_total(days_result, salaries_result, budget_result):
        
        total_costs = {}
        
        for day in days_result:
            
            user_record = day.get('_id',{})
            user_id = user_record.get('user_id')
            project = user_record.get('project')
            user_date = user_record.get('date')
            user_YM = '-'.join(user_date.split('-')[:2])
            user_hours = day.get('hours', 0)
    
            cost = next((sal['salary'][0]['cost'] for sal in salaries_result if sal['_id'] == ObjectId(user_id) and sal['salary'][0]['from'] <= user_date and sal['salary'][0]['to'] >= user_date ), 0)
            
            budget, extra = next(( (budg['_id']['budget'], budg['_id']['extra']) for budg in budget_result if budg['_id']['project_id'] == ObjectId(project) and budg['_id']['period'].startswith(user_YM)), (0,0))
            
            if cost or budget or extra:
                
                if not total_costs.get(user_YM):
                    total_costs[user_YM] = { 'cost' : 0, 'budget' : budget, 'extra' : extra}
             
                total_costs[user_YM]['cost'] = total_costs[user_YM]['cost']  + ( cost * user_hours )
                 
        ## ORDER
        
        output_costs_list = []
        
        for ym in sorted(total_costs.keys()):
            output_costs_list.append( (ym, total_costs[ym]) )
                
        return output_costs_list

    def _merge_by_project(days_result, salaries_result, budget_result):
    
        ### MERGE
        project_costs = {}
        
        for day in days_result:
            
            user_record = day.get('_id',{})
            user_id = user_record.get('user_id')
            project = user_record.get('project')
            user_date = user_record.get('date')
            user_YM = '-'.join(user_date.split('-')[:2])
            user_hours = day.get('hours', 0)
    
            cost = next((sal['salary'][0]['cost'] for sal in salaries_result if sal['_id'] == ObjectId(user_id) and sal['salary'][0]['from'] <= user_date and sal['salary'][0]['to'] >= user_date ), 0)
            
            budget, extra = next(( (budg['_id']['budget'], budg['_id']['extra']) for budg in budget_result if budg['_id']['project_id'] == ObjectId(project) and budg['_id']['period'].startswith(user_YM)), (0,0))
            
            if cost or budget or extra:
                    
                if not project_costs.get(project):
                    project_costs[project] = { user_YM : {}}
                if not project_costs[project].get(user_YM):
                    project_costs[project][user_YM] = { 'cost' : 0, 'budget' : budget, 'extra' : extra}
                    
                # While can exists multiple costs for a project-month, cannot exists multiple badges or extras
                project_costs[project][user_YM]['cost'] = project_costs[project][user_YM]['cost']  + ( cost * user_hours )
             
             
        ## ORDER
        output_costs_dict = {}
        
        for project in project_costs.keys():
            output_costs_dict[project] = []
            
            for ym in sorted(project_costs[project].keys()):
                output_costs_dict[project].append( (ym, project_costs[project][ym]) )    
          
        return output_costs_dict
            

    check_action_permissions('report_projects', 'report_projects')
    validate_request('report_projects', criteria)
    sanified_criteria = sanitize_objectify_json(criteria)
        
    aggregation_mode = sanified_criteria.get('mode', 'total')  

    # Find project list 
    projects_input = _find_project_list_by_customer(sanified_criteria)
    
    # Day mining
    days_result = _find_days_by_projects(projects_input, sanified_criteria)['result'] 
    days_ids_list = [ ObjectId(r['_id']['user_id']) for r in days_result ]
    
    # Salary mining
    salaries_result = _find_salaries_by_date_users(days_ids_list, sanified_criteria['end'], sanified_criteria['start'])['result']

    # Project budget extra mining
    budget_result = _find_costs_by_project_date(projects_input, sanified_criteria['end'], sanified_criteria['start'])['result']

    if aggregation_mode == 'total':
        return { 'records' : _merge_total(days_result, salaries_result, budget_result) }
    
    elif aggregation_mode == 'project':
        return { 'records' : _merge_by_project(days_result, salaries_result, budget_result) }    
