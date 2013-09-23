import cgi, yaml, os
from core.config import schema, core_folder
from validictory import ValidationError, validate
from bson import ObjectId

# Input validation method to prevent XSS 
def sanitize_json(json_record):
    
    sanitized_json = {}
    for key, value in json_record.items():
        if isinstance(value, str):
            sanitized_json[key] = cgi.escape(value, quote=True)
        else:
            sanitized_json[key] = value
        
    return sanitized_json


# Input validation of list of JSON
def sanitize_json_list(json_list):
    
    if not isinstance(json_list, list):
        raise ValidationError("list expected, not '%s'" % json_list.__class__.__name__)
    
    sanitized_list = []
    for json_record in json_list:
        sanitized_list.append(sanitize_json(json_record))

    return sanitized_list

# Convert ObjectId to string in JSON
def stringify_json_with_objectid(json_record):
    if '_id' in json_record and isinstance(json_record['_id'], ObjectId):
        json_record['_id'] = str(json_record['_id'])
    return json_record

# Convert ObjectId to string in JSON list
def stringify_json_list_with_objectid(json_list):
    stringified = []
    if json_list:
        for json_record in json_list:
            stringified.append(stringify_json_with_objectid(json_record))
    return stringified

def stringify_objectid_list(objectid_list):
    stringified = []
    if objectid_list:
        for objid in objectid_list:
            stringified.append(str(objid))
    return stringified
    
# JSON validation method
def validate_sanitize_json(document, json_record):
    validate(json_record, schema[document])
    return sanitize_json(json_record)

# List of JSON validation method
def validate_sanitize_json_list(document, json_list):
    
    if not isinstance(json_list, list):
        raise ValidationError("list expected, not '%s'" % json_list.__class__.__name__)
    
    validated = []
    
    for json_record in json_list:
        validated.append(validate_sanitize_json(document, json_record))
    
    return validated