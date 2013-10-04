import cgi, yaml, random, string, hashlib, collections, types
from core.config import schema, core_folder
from validictory import ValidationError, validate

# Dirty hack to avoid the bug 
# http://stackoverflow.com/questions/10401499/mongokit-importerror-no-module-named-objectid-error
# Old pymongo versions uses pymongo.objectid.ObjectId while new uses bson.ObjectId
try:
    from pymongo.objectid import ObjectId
except ImportError as e:
    from bson import ObjectId

def recursive_replace(container, replace_function):
    t = container.__class__
    
    replaced = replace_function(container)
    
    if replaced != None:
        return replaced
    elif isinstance(container, collections.Mapping):
        return t((x,recursive_replace(container[x], replace_function)) for x in container)
    elif isinstance(container, collections.Iterable):
        # Add other non-replicable iterables here. 
        t = tuple if isinstance(t, (types.GeneratorType,)) else t
        return t(recursive_replace(x, replace_function) for x in container)
    elif isinstance(container, (int, long, float, complex)):
        return container
    else:
        raise ValueError("I don't know how to handle container type: %s" % type(container))


def _replace_function_sanitize_objectify_json(container):
    
    if isinstance(container, collections.Mapping) and '_id' in container and isinstance(container['_id'],basestring):
        # Objectify id string and continue with recursive replace
        container['_id'] = ObjectId(container['_id'])
        t = container.__class__
        return t((x,recursive_replace(container[x], _replace_function_sanitize_objectify_json)) for x in container)
    elif isinstance(container, ObjectId):
        # Leave already converted ObjectId as-is
        return container
    elif isinstance(container, basestring):
        # Quote strings
        return cgi.escape(container, quote=True)

def sanitize_objectify_json(json_in):
    """Sanitize string and convert _ids to ObjectId in JSON"""
    return recursive_replace(json_in, _replace_function_sanitize_objectify_json)

def _replace_function_stringify_objectid_json(container):
    
    if isinstance(container, collections.Mapping) and '_id' in container and isinstance(container['_id'],ObjectId):
        # Objectify id string and continue with recursive replace
        container['_id'] = str(container['_id'])
        t = container.__class__
        return t((x,recursive_replace(container[x], _replace_function_stringify_objectid_json)) for x in container)
    elif isinstance(container, basestring):
        return container

def stringify_objectid_cursor(cursor_in):
    """Convert ObjectId to string in JSON"""
    
    stringified = []
    for json_in in cursor_in:
        stringified.append(recursive_replace(json_in, _replace_function_stringify_objectid_json))
    return stringified

def _replace_function_stringify_objectid_list(container):
    if isinstance(container, ObjectId):
        return str(container)

def stringify_objectid_list(list_in):
    """Convert an ObjectId list to string list"""
    return recursive_replace(list_in, _replace_function_stringify_objectid_list)

def validate_json_list(collection, list_in):
    
    for json_in in list_in:    
        # Validate json schema
        validate(json_in, schema[collection])
   
def update_password_salt_user_list(collection, list_in):
    
    if collection == 'user':
        for json_in in list_in:    
            if 'password' in json_in and json_in['password']:
                update_password_salt_user_json(json_in)
            else:
                raise ValidationError('Expected nonempty password')
        
    return list_in
        
def update_password_salt_user_json(json_in):
    json_in.update(get_password_salt(json_in['password']))

def get_password_salt(password_in):
    """Method to hash password_in and salt, if inserted"""
    
    salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
    password_out = hashlib.sha256( salt + password_in ).hexdigest()
    
    return { 'password': password_out, 'salt' : salt }
    
    
    
    