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

    submitter = db.user.find_one({ '_id':  ObjectId(expence['user_id']) }, 
                                 { '_id' : 0, 'name' : 1, 'surname' : 1, 'email' : 1 })

    notification_data = {
                         'expence_notes': expence['notes'],
                         'expence_objects' : expence.get('objects', {}), # Could miss in trips
                         'expence_type' : expence_type,
                         'submitter_name' : submitter['name'],
                         'submitter_surname' : submitter['surname'],
                         'submitter_email' : submitter['email'],
                         'notification_type': notification_type
                         }

    if expence_type == 'expences':
        notification_data['expence_date'] = expence['date']
    else:
        notification_data['expence_date'] = '%s-%s' % (expence['start'], expence['end'])

    # Try to send notifications with core/notifications/send_*.py functions specified in config.yaml auth section
    notifications_providers = conf_notifications['providers']    
    notifications_results = []
    for provider in notifications_providers:
        
        notifications_module = __import__('core.notifications.notify_%s' % provider, fromlist=["*"])
        notification_error = notifications_module.notify(recipients, notification_data)
        
        if notification_error:
            notifications_results.append(notification_error)

    return notifications_results
    

def get_pending():
    
    # Get flow status number relative to current user
    owner_status = get_role_approval_step(cherrypy.session['_ts_user']['group'])

    aggregations_types = [ 'trips', 'expences']
    
    records = { 'trips' : [], 'expences' : [] }
    
    pending_count = 0
    
    for aggregation_type in aggregations_types:

        # If is administrator, can see whole ranges
        if owner_status == 0:
            match_project_status = { '%s.status' % aggregation_type : { '$gt' : 0 } }
        # If it is a permitted user, can see only specific status
        else:
            match_project_status = { '%s.status' % aggregation_type : owner_status }

            # If user is not in the approvations chain, filter also user_id parameter
        if cherrypy.session['_ts_user']['group'] == 'employee':
            match_project_status.update({ '%s.user_id' % aggregation_type : str(cherrypy.session['_ts_user']['_id']) })


        projects_requested = [ ObjectId(p) for p in cherrypy.session['_ts_user']['managed_projects'] ]
        if projects_requested:
            match_project_status.update({ '_id' : { '$in' : projects_requested } })

        aggregation_pipe = [  
                            { '$unwind' : '$%s' % aggregation_type },
                            { '$match' : match_project_status },
                            { '$group' : { '_id' : None, 'count' : { '$sum' : 1 } } }
        ]

        cherrypy.log('%s' % (aggregation_pipe), context = 'TS.PENDING_NOTIFICATIONS.aggregation_pipe', severity = logging.INFO)

        result = db.project.aggregate(aggregation_pipe)['result']
            
        if result:
            pending_count += result[0]['count']       
        
    return pending_count