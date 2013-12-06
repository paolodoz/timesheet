from core.validation.permissions import get_role_approval_step
from core.api.crud import db
from bson.objectid import ObjectId
from core.notifications import sendmail
from core.config import conf_approval_flow
import cherrypy, logging

def notify_expence(expence, expence_type):
    
    expence['expence_type'] = expence_type
    
    # If expence['status'] <= 0, the mail of one user is approved or rejected.
    # Template used: expence_approved, recipient: user_id 
    if expence['status'] <= 0:
        
        recipients = [ db.user.find_one({ '_id':  ObjectId(expence['user_id']) }, { '_id' : 0, 'name' : 1, 'surname' : 1, 'email' : 1 }) ]
        expence['status_string'] = 'rejected' if expence['status'] < 0 else 'approved'
        
    # Else is a new notification pending for the user
    # Template used: expence_pending, recipient: reposponible of the flow step
    # excluding 0 and flow[-1] that is draft
    elif expence['status'] > 0 and expence['status'] < len(conf_approval_flow)-2:
        
        recipients_group = conf_approval_flow[expence['status']]
        recipients = db.user.find({ 'group':  recipients_group }, { '_id' : 0, 'name' : 1, 'surname' : 1, 'email' : 1 })
        
        # If the recipient in the group is unique (accounting?) send directly
        
        expence['status_string'] = 'pending'
        
        
#    sendmail.sendmail(mail_data)
    
    

def get_pending():
    
    
    # Get flow status number relative to current user
    approval_step = get_role_approval_step(cherrypy.session['_ts_user']['group'])
    
    pending_count = 0
    
    # If approval_step != 0 (admin) count how many pendent notifications
    if approval_step != 0:

        for aggregation_type in [ 'trips', 'expences' ]:

            approval_filters = {}
            approval_filters['_id'] = { '$in' :  [ ObjectId(p) for p in cherrypy.session['_ts_user']['managed_projects'] ] } 
            
            # If user is not in the approvations chain, filter also user_id parameter
            if approval_step == len(conf_approval_flow)-1:
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
        