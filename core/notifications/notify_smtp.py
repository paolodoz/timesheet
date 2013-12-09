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


def notify(recipients, notification_type):

    for user_data in recipients:
        mailmessage = notifications.get_template('%s.tpl' % notification_type).render(**user_data)
        _sendmail(conf_mail['from_address'], user_data['email'], mailmessage)
