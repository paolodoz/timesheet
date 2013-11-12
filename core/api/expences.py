from core.validation.permissions import check_datamine_permissions
from core.validation.validation import TSValidationError, validate_request, update_password_salt_user_list, validate_json_list, sanitize_objectify_json, stringify_objectid_cursor, stringify_objectid_list
from bson.objectid import ObjectId
from core.api.crud import db
import cherrypy, logging

def push_expences(documents_list):
    
    """
    Add new expences in projects
    
    POST /data/push_expences/
    
    Expects a list of 'project' elements having the 'project.expences' subdocument.
    Returns the { 'error' : string, 'ids' : [] }
    """
    
    validate_request('push_expences', documents_list)
    validate_json_list('project', documents_list)
    
    for document in documents_list:
        
        # Check if current user is an employee of selected project
        # TODO: find a better way using standard check_datamine_permissions validation
        if cherrypy.session['_ts_user']['group'] == 'employee':
            found = db.project.find({ '_id' : ObjectId(document['_id']), 'employees._id' : cherrypy.session['_ts_user']['_id'] }).limit(1).count()
            if not found:
                raise TSValidationError("Access to project '%s' is restricted for current user" % (document['_id']))
            
        check_datamine_permissions('push_expences', document)
    
    sanified_documents_list = sanitize_objectify_json(documents_list)
    
    expences_ids = []
    
    cherrypy.log(str(sanified_documents_list), context = 'TS.PUSH_EXPENCES', severity = logging.INFO)
    
    for sanified_document in sanified_documents_list:

        project_id = sanified_document['_id']

        found = db.project.find({ '_id' : project_id }).limit(1).count()

        # If found
        if found:
            for expence in sanified_document['expences']:

                 expence_id = expence.get('_id')
                 if expence_id != None:
                     # If expence._id is already set, drop old expence data
                     db.project.update({'_id': project_id }, {'$pull': {'expences': {'_id': expence_id }}})
                 else:
                     # Else, generate random expence_id             
                     expence_id = ObjectId()
                 
                 expence['_id'] = expence_id
                 
                 # Push new one, only if other elements than _id are provided
                 if len(expence.keys()) > 1:
                     db.project.update({'_id': project_id }, {'$push' : { 'expences' : expence }})

                 expences_ids.append(str(expence_id))

    return { 'ids' : expences_ids }




def search_expences(criteria):
    
    """
    Get expences
    
    POST /data/search_expences/    
    
    Expects { 'start': data, 'end': data, 'status': [ integer, integer, .. ], 'user_id': string, project_id: string, employee_id: string, 'responsible_id' : string }
    Returns { 'error' : string, 'records' : [ { }, { }, .. ]  } 
    """

    validate_request('search_expences', criteria)
    check_datamine_permissions('search_expences', criteria)
    
    sanified_criteria = sanitize_objectify_json(criteria)

    # Prepare the aggregation pipeam
    
    projects_ids_matches = {}
    employee_id = sanified_criteria.get('employee_id')
    if employee_id != None:
        projects_ids_matches['employees._id'] = ObjectId(employee_id)
    responsible_id = sanified_criteria.get('responsible_id')
    if responsible_id != None:
        projects_ids_matches['responsible._id'] = ObjectId(responsible_id)
    project_id = sanified_criteria.get('project_id')
    if project_id != None:
        projects_ids_matches['_id'] = ObjectId(project_id)


    trips_matches = {}
    user_id = sanified_criteria.get('user_id')
    if user_id != None: 
        trips_matches['expences.user_id'] = user_id  
    date_start = sanified_criteria.get('start')
    if date_start != None:
        trips_matches['expences.date'] = { '$gte' : date_start }
    date_end = sanified_criteria.get('end')
    if date_end != None:
        trips_matches['expences.date'] = { '$lte' : date_end }
    status = sanified_criteria.get('status')
    if status != None:
        trips_matches['expences.status'] = { '$in' : status }

    aggregation_pipe = [  
                        { '$match': projects_ids_matches },
                        { '$unwind' : '$expences' }, 
                        { '$match' : trips_matches },
                        { '$group' : { '_id' : '$expences' } }
                        ]


    cherrypy.log('%s' % (aggregation_pipe), context = 'TS.SEARCH_EXPENCES.aggregation_pipe', severity = logging.INFO)
    
    aggregation_result = db.project.aggregate(aggregation_pipe)

    return { 'records' : stringify_objectid_cursor([ record['_id'] for record in aggregation_result['result'] ]) }


