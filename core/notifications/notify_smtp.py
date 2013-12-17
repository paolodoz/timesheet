import smtplib
from core.config import conf_notifications, notifications

conf_mail = conf_notifications['smtp']

def _sendmail(fromaddr, toaddrs, mail):

    header = ("From: %s\r\nTo: %s\r\n\r\n"
           % (fromaddr, ", ".join(toaddrs)))
    
    message = header + mail
    
    server = smtplib.SMTP(conf_mail['host'])
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, message)
    server.quit()


def notify(recipients, notification_data):

    for recipient_data in recipients:
        
        notification_data['recipient_name'] = recipient_data['name']
        notification_data['recipient_surname'] = recipient_data['surname']
        notification_data['recipient_email'] = recipient_data['email']
        
        mailmessage = notifications.get_template('%s.tpl' % notification_data['notification_type']).render(**notification_data)
        _sendmail(conf_mail['from_address'], [ notification_data['recipient_email'] ], mailmessage)
