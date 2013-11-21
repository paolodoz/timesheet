from core.validation.validation import validate_request
from core.validation.permissions import check_datamine_permissions
from core.api.crud import db
import cherrypy, logging
 
def search_tags(criteria):
     
    """
    Collect tags
     
    POST /data/search_tags/    
     
    Expects { 'count' : int }
    Returns { 'error' : string, 'records' : [ 'tag1', 'tag2', ... ]  } 
    """
    
    validate_request('search_tags', criteria)
    check_datamine_permissions('search_tags', criteria)
 
    aggregation_pipe = [  
                        { '$unwind' : '$tags' }, 
                        { '$group' : { '_id' : '$tags', 'count' : { '$sum' : 1 } } }, 
                        { '$sort' : { 'count' : -1 } },
                        { '$limit' : criteria['count'] }
                        ]
 
    cherrypy.log('%s' % (aggregation_pipe), context = 'TS.SEARCH_TRIPS.aggregation_pipe', severity = logging.INFO)
     
    aggregation_result = db.project.aggregate(aggregation_pipe)
 
    return { 'records' : [ record['_id'] for record in aggregation_result['result'] ] }
