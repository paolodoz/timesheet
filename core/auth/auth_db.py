import hashlib
from core.api.crud import db

def check_credentials(username, password_in):
    """User authentication based on database user collection"""
    
    user_record = db['user'].find_one({ 'username' : username }, { '_id' : 1, 'password' : 1, 'salt' : 1 })

    if user_record:
        password_db = user_record.get('password', '')
        salt = user_record.get('salt', '')
        
        if salt and password_db and password_db == hashlib.sha256( salt + password_in ).hexdigest():
            return None
           
    return u"Incorrect username or password."