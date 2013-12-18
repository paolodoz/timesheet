import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.config import conf_notifications, notifications



conf_mail = conf_notifications['smtp']

def _sendmail(fromaddr, toaddrs, text, html, subject):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddrs)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP(conf_mail['host'])
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

def _compose_mail(notification_data):
    text = notifications.get_template('%s.tpl' % conf_mail['template_text']).render(**notification_data)
    html = notifications.get_template('%s.tpl' % conf_mail['template_html']).render(**notification_data)

    if notification_data['notification_type'] == 'notify_new':
        subject = 'Timesheet: new expence request for %s from %s' % (notification_data['project_name'], 
                                                                     notification_data['submitter_email'])
    elif notification_data['notification_type'] == 'notify_reject':
        subject = 'Timesheet: expence for %s rejected by %s' % (notification_data['project_name'], 
                                                                notification_data['approver_email'])
    elif notification_data['notification_type'] == 'notify_approve':
        subject = 'Timesheet: expence for %s approved by %s' % (notification_data['project_name'], 
                                                                notification_data['approver_email'])

    return text, html, subject

def notify(recipients, notification_data):

    for recipient_data in recipients:
        
        notification_data['recipient_name'] = recipient_data['name']
        notification_data['recipient_surname'] = recipient_data['surname']
        notification_data['recipient_email'] = recipient_data['email']
        
        text, html, subject = _compose_mail(notification_data)
        _sendmail(conf_mail['from_address'], [ notification_data['recipient_email'] ], text, html, subject)
    
