from core.config import conf_notifications, notifications

def notify(recipients, notification_type):

    notifications_result = {}

    for user_data in recipients:
        notifications_result[user_data['email']] = notifications.get_template('%s.tpl' % notification_type).render(**user_data)

    return notifications_result
        
        
