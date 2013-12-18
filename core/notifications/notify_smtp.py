import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.config import conf_notifications, notifications



conf_mail = conf_notifications['smtp']

def _sendmail(fromaddr, toaddrs, text, subject):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddrs

    part1 = MIMEText(text, 'plain')
    #part2 = MIMEText(html, 'html')
    
    msg.attach(part1)
    #msg.attach(part2)

    server = smtplib.SMTP(conf_mail['host'])
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

def _generate_mail(notification_data):
    message = notifications.get_template('%s.tpl' % conf_mail['template']).render(**notification_data)
    subject = 'Timesheet %s' % (notification_data['name'])

    return message, subject

def notify(recipients, notification_data):

    for recipient_data in recipients:
        
        notification_data['recipient_name'] = recipient_data['name']
        notification_data['recipient_surname'] = recipient_data['surname']
        notification_data['recipient_email'] = recipient_data['email']
        
        message, subject = _generate_mail(notification_data)
        _sendmail(conf_mail['from_address'], [ notification_data['recipient_email'] ], message, subject)
    
