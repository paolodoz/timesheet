from core.config import conf_notifications, notifications

conf_debug = conf_notifications['debug']

def notify(recipients, notification_data):

    notifications_result = {}

    for recipient_data in recipients:
        notification_data['recipient_name'] = recipient_data['name']
        notification_data['recipient_surname'] = recipient_data['surname']
        notification_data['recipient_email'] = recipient_data['email']

        notifications_result[notification_data['recipient_email']] = notifications.get_template('%s.tpl' % conf_debug['template']).render(**notification_data)
    
    return notifications_result    
    