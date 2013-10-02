import cgi, yaml, random, string, hashlib
from core.config import schema, core_folder
from validictory import ValidationError, validate

# Dirty hack to avoid the bug 
# http://stackoverflow.com/questions/10401499/mongokit-importerror-no-module-named-objectid-error
# Old pymongo versions uses pymongo.objectid.ObjectId while new uses bson.ObjectId
try:
    from pymongo.objectid import ObjectId
except ImportError as e:
    from bson import ObjectId

def validate_criteria_projection(criteria_projection):
    
    if not isinstance(criteria_projection, list) or not len(criteria_projection) == 2:
        raise ValidationError('Bad criteria and projection list' )
         
    if not criteria_projection[1]:
        raise ValidationError('Filter projection cannot be empty')

    return criteria_projection

def sanitize_json(json_record):
    """Input validation method to prevent XSS"""
    sanitized_json = {}
    for key, value in json_record.items():
        if isinstance(value, str):
            sanitized_json[key] = cgi.escape(value, quote=True)
        else:
            sanitized_json[key] = value
        
    return sanitized_json


def sanitize_json_list(json_list):
    """Input validation of list of JSON"""
    if not isinstance(json_list, list):
        raise ValidationError("List expected, not '%s'" % json_list.__class__.__name__)
    
    sanitized_list = []
    for json_record in json_list:
        sanitized_list.append(sanitize_json(json_record))

    return sanitized_list


def objectify_json_with_idstring(json_record):
    """Convert string to ObjectId in JSON"""
    if '_id' in json_record and isinstance(json_record['_id'], basestring):
        json_record['_id'] = ObjectId(json_record['_id'])
    return json_record


def stringify_json_with_objectid(json_record):
    """Convert ObjectId to string in JSON"""

    if '_id' in json_record and isinstance(json_record['_id'], ObjectId):
        json_record['_id'] = str(json_record['_id'])
        
    return json_record

def stringify_json_list_with_objectid(json_list):
    """Convert ObjectId to string in JSON list"""
    stringified = []
    if json_list:
        for json_record in json_list:
            stringified.append(stringify_json_with_objectid(json_record))
    return stringified

def stringify_objectid_list(objectid_list):
    """Convert an ObjectId list to string list"""
    stringified = []
    if objectid_list:
        for objid in objectid_list:
            stringified.append(str(objid))
    return stringified
    
def validate_transform_json(collection, json_record):

    # Validate json schema
    validate(json_record, schema[collection])
    
    # Sanitize user input
    json_record.update(sanitize_json(json_record))
    
    # If in user collection, calculate password and salt
    if collection == 'user' and json_record['password']:
        json_record.update(calculate_password_and_salt_in_json_user(json_record['password']))
            
    return json_record

def validate_transform_json_list(collection, json_list):
    """JSON list validation and transformation method"""
    
    if not isinstance(json_list, list):
        raise ValidationError("List expected, not '%s'" % json_list.__class__.__name__)
    
    for json_record in json_list:
        json_record = validate_transform_json(collection, json_record)
    
    return json_list

def calculate_password_and_salt_in_json_user(password_in):
    """Method to hash password_in and salt, if inserted"""
    
    salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
    password_out = hashlib.sha256( salt + password_in ).hexdigest()
    
    return { 'password': password_out, 'salt' : salt }
    
    
    
    