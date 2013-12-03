from core.validation.permissions import approval_flow
from core.api.crud import db
from bson.objectid import ObjectId
import cherrypy, logging

def get_pending():
    
    
    # Get flow status number relative to current user
    approval_step, approval_name = approval_flow(cherrypy.session['_ts_user']['group'])
    
    pending_count = 0
    
    # If approval_step != 0 (admin) count how many pendent notifications
    if approval_step != 0:

        for aggregation_type in [ 'trips', 'expences' ]:

            approval_filters = {}
            approval_filters['_id'] = { '$in' :  [ ObjectId(p) for p in cherrypy.session['_ts_user']['managed_projects'] ] } 
            
            # If user is not in the approvations chain, filter also user_id parameter
            if approval_name == 'draft':
                approval_filters['%s.user_id' % aggregation_type] = str(cherrypy.session['_ts_user']['_id'])

        
            approval_filters['%s.status' % aggregation_type] = approval_step

            cherrypy.log('%s' % ([ { '$unwind' : '$%s' % aggregation_type }, { '$match' : approval_filters }]), 
                         context = 'TS.PENDING_NOTIFICATIONS.aggregation_pipe', severity = logging.INFO)

            result = db.project.aggregate([  
                                { '$unwind' : '$%s' % aggregation_type },
                                { '$match' : approval_filters },
                                { '$group' : { '_id' : None, 'count' : { '$sum' : 1 } } }
            ])['result']
            
            if result:
                pending_count += result[0]['count']

    return pending_count
        