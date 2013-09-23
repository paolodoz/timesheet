from core.db import db
from core.validation import validate_sanitize_json, validate_sanitize_json_list, sanitize_json, sanitize_json_list, stringify_objectid_list, stringify_json_list_with_objectid
from bson.objectid import ObjectId

# Get selected records from collection, and return it as json
# Called by GET /<collection>/
def get(collection, selection = {}):
    
    if '_id' in selection:
        selection['_id'] = ObjectId(selection['_id'])
    
    return stringify_json_list_with_objectid(db[collection].find(sanitize_json(selection)))

# Remove selected records from collection
# Called by POST /remove/<collection>
def remove(collection, selections = []):
    for selection in selections:
        db[collection].remove(sanitize_json(selection))
            
    
# Insert new record list to collection
# Called by POST /add/<collection>/
def add(collection, elements_list):
    return stringify_objectid_list(db[collection].insert(validate_sanitize_json_list(collection, elements_list)))

    