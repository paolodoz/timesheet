from core.db import db
import hashlib

def check_ldap_credentials(username, password):
    """User authentication based on LDAP"""
    return u"Incorrect username or password."

def check_db_credentials(username, password_in):
    """User authentication based on database user collection"""
    
    user_record = db['user'].find_one({ 'username' : username }, { '_id' : 1, 'password' : 1, 'salt' : 1 })
    if user_record:
        password_db = user_record.get('password', '')
        salt = user_record.get('salt', '')
        
        if salt and password_db and password_db == hashlib.sha256( salt + password_in ).hexdigest():
            return None
           
    return u"Incorrect username or password."