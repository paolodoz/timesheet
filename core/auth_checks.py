from core.db import db
import hashlib

def check_ldap_credentials(username, password):
    """User authentication based on LDAP"""
    return u"Incorrect username or password."

def check_db_credentials(username, password):
    """User authentication based on database user collection"""
    
    user_record = db['users'].find_one({ 'username' : username }, { '_id' : 1 })
    if user_record:
        user_id = user_record.get('_id', None)
        
        if user_id:
           password_record = db['password'].find_one({ 'user_id' : user_id }, { 'salt' : 1, 'key' : 1})
           if password_record:
               password_salt = password_record.get('salt', None)
               password_key = password_record.get('key', None)
               if password_salt and password_key and password_key == hashlib.sha256( password_salt + password ).hexdigest():
                    return None
           
    return u"Incorrect username or password."