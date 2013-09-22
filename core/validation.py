import cgi, validictory, yaml, os
from core.config import schema, core_folder


# Input validation method to prevent XSS 
def sanitize_json(json):
    
    sanitized_json = {}
    for key, value in json.items():
        sanitized_json[key] = cgi.escape(value, quote=True)
        
    return sanitized_json


# Validate against schema saved in yaml
def _validate_schema(document, json):
    validictory.validate(json, schema[document])
    
# JSON validation method
def validate(document, json):
    _validate_schema(document, json)
    return sanitize_json(json)