from core.validation.permissions import get_role_approval_step
from core.api.crud import db
from bson.objectid import ObjectId
from core.config import conf_approval_flow, conf_notifications
import cherrypy, logging

def _get_recipients_of_expences_responsibles(expence_user_id, project_id, expence_id, expence_type, recipients_roles ):

    recipients = []

    for role in recipients_roles:
    
        # If role is submitter, send mail to the submitter user
        if role == '%submitter%':
            recipients += [ db.user.find_one({ '_id':  ObjectId(expence_user_id) }, { '_id' : 0, 'name' : 1, 'surname' : 1, 'email' : 1 }) ]
        else:
            # Find the ids of all the responsibles of the project
            
            aggregation_pipe = [  
                    { '$unwind' : '$%s' % expence_type },
                    { '$unwind' : '$responsibles' },
                    { '$match' : { '_id':  ObjectId(project_id), 
                                  '%s._id' % expence_type : ObjectId(expence_id), 
                                  'responsibles.role' : role  } },
                    { '$group' : { '_id' : '$responsibles._id' } 
                    }
            ]
            
            cherrypy.log('%s' % (aggregation_pipe), context = 'TS.NOTIFY_EXPENCE.aggregation_pipe', severity = logging.INFO)
            
            responsibles = db.project.aggregate(aggregation_pipe)['result']
            
            recipients += list(db.user.find({ '_id':  {  '$in' : [ ObjectId(responsible['_id']) for responsible in responsibles ] } }, { '_id' : 0, 'name' : 1, 'surname' : 1, 'email' : 1 }))

    return recipients


def notify_expence(expence, project_id, expence_type):
    
    
    # If current status is >= 0, notify the new expence
    if expence['status'] >= 0:
        notification_type = 'notify_new'
    else:
        notification_type = 'notify_reject'
        
    recipients_roles = conf_approval_flow[expence['status']].get(notification_type,[])

    recipients = _get_recipients_of_expences_responsibles(expence_user_id = expence['user_id'], 
                                                         project_id = project_id, 
                                                         expence_id = expence['_id'], 
                                                         expence_type = expence_type, 
                                                         recipients_roles = recipients_roles)

    # Try to send notifications with core/notifications/send_*.py functions specified in config.yaml auth section
    notifications_providers = conf_notifications['providers']    
    notifications_results = []
    for provider in notifications_providers:
        
        notifications_module = __import__('core.notifications.notify_%s' % provider, fromlist=["*"])
        notification_error = notifications_module.notify(recipients, notification_type)
        
        if notification_error:
            notifications_results.append(notification_error)

    return notifications_results
    

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
            if cherrypy.session['_ts_user']['group'] == 'employee':
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
        