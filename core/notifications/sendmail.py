import smtplib
from core.config import conf_mail, mails

def _sendmail(fromaddr, toaddrs, mail):

    header = ("From: %s\r\nTo: %s\r\n\r\n"
           % (fromaddr, ", ".join(toaddrs)))
    
    message = header + mail
    
    server = smtplib.SMTP(conf_mail['smtp'])
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, message)
    server.quit()


def sendmail(recipient_data, template = 'new_expence'):

    mailmessage = mails.get_template('%s.tpl' % template).render(**recipient_data)
    
    _sendmail(conf_mail['address'], recipient_data['email'], mailmessage)
