from core.validation.validation import TSValidationError, validate_request, update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from core.validation.permissions import check_datamine_permissions
from core.config import conf_reports, conf_approved
from bson.objectid import ObjectId
from core.api.crud import db
import cherrypy, logging


def report_projects(criteria):
    
    """
    Get projects report
    
    POST /data/report_projects/
    
    Expects { 'start' : '', 'end' : '', 'customers' : [], 'projects' : [], 'tags' : [], 'mode' : 'total|project' } 
    Returns with mode total
       { 'error' : string, 'records' : [ [ 'YYYY-MM', 2 ], [ 'YYYY-MM', 4 ], .. ]  } 
    Returns with mode total
       { 'error' : string, 'records' : {  'proj1' : [ [ 'YYYY-MM', 2 ], [ 'YYYY-MM', 4 ] ], .. }  } 
    """
    
    def _find_project_list_by_customers_types(sanified_criteria):
        
        projects_input = sanified_criteria.get('projects', [])
        
        # Add projects by customers
        customers_input = sanified_criteria.get('customers')
        if customers_input:
            customer_projects = db.project.find( { 'customer' : {  '$in' : customers_input } }, { '_id' : 1 })
            for project in customer_projects:
                projects_input.append(str(project['_id'])) 
            
        # Add projects by tags
        types_input = sanified_criteria.get('tags')
        if types_input:
            types_projects = db.project.find( { 'tags' : {  '$in' : types_input } }, { '_id' : 1 })
            for project in types_projects:
                projects_input.append(str(project['_id'])) 
        
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
        
        check_datamine_permissions('report_projects', match_projects)
        
        aggregation_pipe = [ 
                            { '$match': dates_match },
                            { '$unwind' : '$users' }, 
                            { '$unwind' : '$users.hours' }, 
                            { '$match' : match_projects },
                             { '$group' : 
                              { '_id' : { 
                                         'user_id' : '$users.user_id', 
                                         'date' : '$date',
                                         'project' : '$users.hours.project',
                                         'isextra' : '$users.hours.isextra'
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

    def _find_incomes_by_project_date(projects_input, end, start):

        objectified_projects_input = [ ObjectId(p) for p in projects_input ]

        if projects_input:
            match_projects = { '_id' : { '$in' : objectified_projects_input }  }
        else:
            match_projects = {}

        aggregation_pipe = [ { '$match' : match_projects }, { '$unwind' : '$economics'}, { '$match' : { 'economics.period' : { '$gte' : start, '$lte' : end } } }, { '$group' : { '_id' : { 'project_id' : '$_id', 'period' : '$economics.period', 'budget' : '$economics.budget', 'extra' : '$economics.extra'   } } } ]
        cherrypy.log(aggregation_pipe.__repr__(), context = 'TS.REPORT_PROJECTS.incomes_aggregation', severity = logging.INFO)
        return db.project.aggregate(aggregation_pipe)

    def _find_costs_by_project_date(projects_input, end, start):

        objectified_projects_input = [ ObjectId(p) for p in projects_input ]

        if projects_input:
            match_projects = { '_id' : { '$in' : objectified_projects_input }  }
        else:
            match_projects = {}

        aggregation_pipe = [ { '$match' : match_projects }, 
                            { '$unwind' : '$expences'}, 
                            { '$match' : { 'expences.status' : conf_approved } }, 
                            { '$unwind' : '$expences.objects'}, 
                            { '$match' : { 'expences.objects.date' : { '$gte' : start, '$lte' : end } } }, 
                            { '$group' : { '_id' : { 'project_id' : '$_id', 
                                                    'date' : '$expences.objects.date'
                                                    },
                                          
                                           'amount' : { '$sum' : '$expences.objects.amount'  } 
                                           } 
                             } 
                            ]
        cherrypy.log(aggregation_pipe.__repr__(), context = 'TS.REPORT_PROJECTS.costs_aggregation', severity = logging.INFO)
        return db.project.aggregate(aggregation_pipe)


    def _merge_total(days_result, salaries_result, budget_result, costs_result):
        
        total_costs = {}
        
        for day in days_result:
            
            user_hours_record = day.get('_id',{})
            user_id = user_hours_record.get('user_id')
            project = user_hours_record.get('project')
            isextra = user_hours_record.get('isextra')
            user_date = user_hours_record.get('date')
            user_YM = '-'.join(user_date.split('-')[:2])
            user_hours = day.get('hours', 0)
    
            salary = next((sal['salary'][0]['cost'] for sal in salaries_result if sal['_id'] == ObjectId(user_id) and sal['salary'][0]['from'] <= user_date and sal['salary'][0]['to'] >= user_date ), 0)
            
            if salary:

                # If the hour block is extra, add the multiplier_on_extras to itself
                if isextra:
                    salary *= conf_reports['multiplier_on_extras']

                if not total_costs.get(user_YM):
                    total_costs[user_YM] = { 'salary' : 0, 'budget' : 0, 'extra_budget' : 0, 'costs' : 0}
             
                total_costs[user_YM]['salary'] = total_costs[user_YM]['salary']  + round( salary * user_hours, 2 )
        
        for budget in budget_result:
            budget_YM = '-'.join(budget['_id']['period'].split('-')[:2])
            
            if not total_costs.get(budget_YM):
                 total_costs[budget_YM] = { 'salary' : 0, 'budget' : 0, 'extra_budget' : 0, 'costs' : 0}
            
            total_costs[budget_YM]['budget'] = budget['_id']['budget']
            total_costs[budget_YM]['extra_budget'] = budget['_id']['extra']

        for costs in costs_result:
            costs_YM = '-'.join(costs['_id']['date'].split('-')[:2])
            
            if not total_costs.get(costs_YM):
                 total_costs[costs_YM] = { 'salary' : 0, 'budget' : 0, 'extra_budget' : 0, 'costs' : 0}
            
            total_costs[costs_YM]['costs'] = costs['amount']            
                 
        ## ORDER
        
        output_costs_list = []
        
        for ym in sorted(total_costs.keys()):
            output_costs_list.append( (ym, total_costs[ym]) )
                
        return output_costs_list

    def _merge_by_project(days_result, salaries_result, budget_result, costs_result):
    
        ### MERGE
        project_costs = {}
        
        for day in days_result:
            
            user_hours_record = day.get('_id',{})
            user_id = user_hours_record.get('user_id')
            project = user_hours_record.get('project')
            isextra = user_hours_record.get('isextra')
            user_date = user_hours_record.get('date')
            user_YM = '-'.join(user_date.split('-')[:2])
            user_hours = day.get('hours', 0)
    
            salary = next((sal['salary'][0]['cost'] for sal in salaries_result if sal['_id'] == ObjectId(user_id) and sal['salary'][0]['from'] <= user_date and sal['salary'][0]['to'] >= user_date ), 0)
            
            if salary:
                    
                if not project_costs.get(project):
                    project_costs[project] = { user_YM : {}}
                if not project_costs[project].get(user_YM):
                    project_costs[project][user_YM] = { 'salary' : 0, 'budget' : 0, 'extra_budget' : 0, 'costs' : 0}
                
                # If the hour block is extra, add the multiplier_on_extras to itself
                if isextra:
                    salary *= conf_reports['multiplier_on_extras']
                
                # While can exists multiple costs for a project-month, cannot exists multiple badges or extras
                project_costs[project][user_YM]['salary'] = project_costs[project][user_YM]['salary']  + round( salary * user_hours, 2 )
        
        for budget in budget_result:
            budget_YM = '-'.join(budget['_id']['period'].split('-')[:2])
            project = str(budget['_id']['project_id'])
            
            if not project_costs.get(project):
                project_costs[project] = { budget_YM : {}}
            if not project_costs[project].get(budget_YM):
                project_costs[project][budget_YM] = { 'salary' : 0, 'budget' : 0, 'extra_budget' : 0, 'costs' : 0}
            
            project_costs[project][budget_YM]['budget'] = budget['_id']['budget']
            project_costs[project][budget_YM]['extra_budget'] = budget['_id']['extra']        

        for costs in costs_result:
            costs_YM = '-'.join(costs['_id']['date'].split('-')[:2])
            project = str(costs['_id']['project_id'])
            
            if not project_costs.get(project):
                project_costs[project] = { costs_YM : {}}
            if not project_costs[project].get(costs_YM):
                project_costs[project][costs_YM] = { 'salary' : 0, 'budget' : 0, 'extra_budget' : 0, 'costs' : 0}
            
            project_costs[project][costs_YM]['costs'] += costs['amount']
             
        ## ORDER
        output_costs_dict = {}
        
        for project in project_costs.keys():
            output_costs_dict[project] = []
            
            for ym in sorted(project_costs[project].keys()):
                output_costs_dict[project].append( (ym, project_costs[project][ym]) )    
          
        return output_costs_dict
            

    validate_request('report_projects', criteria)
    sanified_criteria = sanitize_objectify_json(criteria)
        
    aggregation_mode = sanified_criteria.get('mode', 'total')  

    # Find project list 
    projects_input = _find_project_list_by_customers_types(sanified_criteria)
    
    # Day mining
    days_result = _find_days_by_projects(projects_input, sanified_criteria)['result'] 
    days_ids_list = [ ObjectId(r['_id']['user_id']) for r in days_result ]
    
    # Salary mining
    salaries_result = _find_salaries_by_date_users(days_ids_list, sanified_criteria['end'], sanified_criteria['start'])['result']

    # Project budget extra mining
    budget_result = _find_incomes_by_project_date(projects_input, sanified_criteria['end'], sanified_criteria['start'])['result']

    # Cost mining
    costs_result = _find_costs_by_project_date(projects_input, sanified_criteria['end'], sanified_criteria['start'])['result']

    if aggregation_mode == 'total':
        return { 'records' : _merge_total(days_result, salaries_result, budget_result, costs_result) }
    
    elif aggregation_mode == 'project':
        return { 'records' : _merge_by_project(days_result, salaries_result, budget_result, costs_result) }    
