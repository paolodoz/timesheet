from core.config import conf_notifications, notifications

def notify(recipients, notification_data):


    notifications_result = {}

    for recipient_data in recipients:
        
        notification_data['recipient_name'] = recipient_data['name']
        notification_data['recipient_surname'] = recipient_data['surname']
        notification_data['recipient_email'] = recipient_data['email']
        
        notifications_result[notification_data['recipient_email']] = notifications.get_template('%s.tpl' % notification_data['notification_type']).render(**notification_data)

    return notifications_result    
    