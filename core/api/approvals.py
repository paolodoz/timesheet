from core.validation.validation import TSValidationError, validate_request, sanitize_objectify_json, stringify_objectid_cursor
from core.api.crud import db
from bson.objectid import ObjectId
from core.validation.permissions import approval_flow
from core.config import schema 
import cherrypy, logging

def approval(criteria):
    
    """
    Approve or reject an expence
    
    POST /data/approval/
    
    Expects { 'project_id' : string, 'expence_id|trip_id' : string, 'action': approve|reject, 'note' : string  }
    Returns { 'error' : string, 'status' : integer }
    """
    
    validate_request('approval', criteria)
    sanified_criteria = sanitize_objectify_json(criteria)

    # Current user can approve only approvals with status >= conf_approval_flow.index(group)
    owner_status = approval_flow(cherrypy.session['_ts_user']['group'])

    # Is searching found_expence or trip
    exp_id = sanified_criteria.get('expence_id')
    trp_id = sanified_criteria.get('trip_id')
    expence_type = 'expences' if exp_id else 'trips'
    expence_id = exp_id if exp_id else trp_id
    
    search_criteria = { 
                        '_id' : ObjectId(criteria['project_id']),
                        '%s._id' % expence_type : ObjectId(expence_id),
                        '%s.status' % expence_type : { '$gte' : owner_status } 
                        }
    
    search_projection = { '_id' : 0 , '%s' % expence_type : { '$elemMatch' : { '_id' : ObjectId(expence_id)  } } }

    
    found_expence = db.project.find_one( search_criteria , search_projection)
    original_found_expence = found_expence.copy()
    if not found_expence:
        raise TSValidationError("Can't found selected expence")
    
    # Approved
    if sanified_criteria['action'] == 'approve':
        if found_expence[expence_type][0]['status'] > 0:
            found_expence[expence_type][0]['status'] -= 1
    # Rejected
    else:
        found_expence[expence_type][0]['status'] = -abs(found_expence[expence_type][0]['status'])

    if 'note' in sanified_criteria and sanified_criteria['note']:
        if not 'notes' in found_expence[expence_type][0]:
            found_expence[expence_type][0]['notes'] = []
        found_expence[expence_type][0]['notes'].append(sanified_criteria['note'])

    cherrypy.log('%s\n%s' % (search_criteria, found_expence), context = 'TS.APPROVALS.criteria_projection', severity = logging.INFO)
    
    # Pull the original element
    db.project.update({ '_id' : ObjectId(criteria['project_id'])}, { '$pull' : { expence_type : { '_id' : ObjectId(expence_id)} } } )
    # Push the modified element, with an hack to avoid to push the entire array
    db.project.update({ '_id' : ObjectId(criteria['project_id']) }, { '$push' : { expence_type : found_expence[expence_type][0] } } )
     
    return { 'status' : found_expence[expence_type][0]['status'] }


def search_approvals(criteria):
    
    """
    Search pending expences
    
    POST /data/search_approvals/
    
    Expects { 'project_id' : string, 'type': trips|expences, 'status': rejected|any  }
    Returns { 'error' : string, 'records' : [] }
    """
    
    validate_request('search_approvals', criteria)
    sanified_criteria = sanitize_objectify_json(criteria)

    # Current user can approve only approvals with status >= conf_approval_flow.index(group)
    owner_status = approval_flow(cherrypy.session['_ts_user']['group'])

    type_requested = sanified_criteria.get('type', 'any' )
    if type_requested == 'any':
        aggregations_types = [ 'trips', 'expences']
    else:
        aggregations_types = [ type_requested ]
    
    records = { 'trips' : [], 'expences' : [] }
    
    for aggregation_type in aggregations_types:

        status_requested = sanified_criteria.get('status', 'approved')
        if status_requested == 'approved':
            match_project_status = { '%s.status' % aggregation_type : { '$gte' : owner_status } }
        elif status_requested == 'rejected':
            match_project_status = { '%s.status' % aggregation_type : { '$lte' : -abs(owner_status if owner_status else 1)  } }
        else:
            match_project_status = { '$or' : [  { '%s.status' % aggregation_type : { '$gte' : owner_status } }, 
                                                { '%s.status' % aggregation_type : { '$lte' : -abs(owner_status if owner_status else 1) } } 
                                            ] } 

        project_requested = sanified_criteria.get('project_id')
        if project_requested:
            match_project_status.update({ '_id' : ObjectId(project_requested) })

        project_rename = { '%s.project_id' % aggregation_type : '$_id' }
        for key in schema['project']['properties'][aggregation_type]['items']['properties'].keys():
            project_rename['%s.%s' % (aggregation_type, key)] = 1

        aggregation_pipe = [  
                            { '$unwind' : '$%s' % aggregation_type },
                            { '$match' : match_project_status },
                            { '$project' : project_rename },
                            { '$group' : { '_id' : '$%s' % (aggregation_type) } },
                            { '$sort' : { '_id.start' : 1, '_id.date' : 1 } }
        ]

        cherrypy.log('%s' % (aggregation_pipe), context = 'TS.SEARCH_APPROVALS.aggregation_pipe', severity = logging.INFO)

        aggregation_result = db.project.aggregate(aggregation_pipe)
        records[aggregation_type] = stringify_objectid_cursor([ record['_id'] for record in aggregation_result['result'] ])

    return records