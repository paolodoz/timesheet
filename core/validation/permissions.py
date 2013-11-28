import yaml, cherrypy, types, jsonschema
from core.validation.validation import TSValidationError, recursive_replace, ObjectId
from core.config import restrictions_schema, conf_approval_flow

def _unique_keeping_order(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def approval_flow(group):

    if group == 'administrator':
        return 0
    elif group in conf_approval_flow:
        return conf_approval_flow.index(group)
    else:
        return 100
    

def get_user_restrictions():
    """Format restriction schemas. Saved on auth login to speedup following accesses"""
    
    
    # Recursively replace needs a condition_function and replace_function
    replacements = { 
                    '%%username%%' : '^%s$' % (cherrypy.session['_ts_user']['username']), 
                    '%%_id%%' : '^%s$' % (str(cherrypy.session['_ts_user']['_id'])),
                    '%%managed_projects%%' : (cherrypy.session['_ts_user']['managed_projects']),
                    '%%employed_projects%%' : (cherrypy.session['_ts_user']['employed_projects']),
                    '%%projects%%' : _unique_keeping_order(cherrypy.session['_ts_user']['employed_projects'] + 
                                          cherrypy.session['_ts_user']['managed_projects']),
                    '%%approval_flow%%' : approval_flow(cherrypy.session['_ts_user']['group']),
                    }

    def _replace_function_permissions_schema(container):
        if isinstance(container,basestring):
            replacement = replacements.get(container)
            if replacement:
                # Replace strings and objectid with string
                if isinstance(replacement,(basestring, ObjectId)):
                    return str(replacement)
                # Replace managed_projects with project list
                elif isinstance(replacement, types.ListType):
                    return replacement
                else:
                    return replacement
        
    formatted_schemas = {}
    
    for collection_name, collection_schema in restrictions_schema.items():
        try:
            group_schema = collection_schema[cherrypy.session['_ts_user']['group']]
        except (KeyError, TypeError):
            pass
        else:
            formatted_schemas[collection_name] = recursive_replace(group_schema, _replace_function_permissions_schema)
    
    return formatted_schemas


def check_datamine_permissions(action, document):
    # Get datamine permissions
    
    if cherrypy.session['_ts_user']['group'] == 'administrator': return
    
    try:
        restrictions = cherrypy.session['_ts_user']['restrictions'][action]
    except (KeyError, TypeError):
        restrictions = None
        
    if not restrictions:
        raise TSValidationError("Access to '%s' is restricted for current user" % (action))
    elif restrictions != True:
        jsonschema.validate(document, restrictions, format_checker=jsonschema.FormatChecker())    
    
def check_remove_permissions(collection, document):
    
    if cherrypy.session['_ts_user']['group'] == 'administrator': return
    
    # Get remove permissions
    try:
        restrictions = cherrypy.session['_ts_user']['restrictions'][collection]['remove']
    except (KeyError, TypeError):
        restrictions = None
        
    if not restrictions:
        raise TSValidationError("Access to 'remove.%s' is restricted for current user" % (collection))
    elif restrictions != True:       
        jsonschema.validate(document, restrictions, format_checker=jsonschema.FormatChecker())
    
def check_upsert_permissions(action, collection, document):
    
    if cherrypy.session['_ts_user']['group'] == 'administrator': return
    
    # Get add/update permissions
    try:
        restrictions = cherrypy.session['_ts_user']['restrictions'][collection][action]
    except (KeyError, TypeError):
        restrictions = None
        
    if not restrictions:
        raise TSValidationError("Access to '%s.%s' is restricted for current user" % (action, collection))
    elif restrictions != True:       
        jsonschema.validate(document, restrictions, format_checker=jsonschema.FormatChecker())

def check_get_permissions(collection, criteria, projection, sort):

    if cherrypy.session['_ts_user']['group'] == 'administrator': return
    
    # Get criteria permissions
    try:
        criteria_restrictions = cherrypy.session['_ts_user']['restrictions'][collection]['get']['criteria']
    except (KeyError, TypeError):
        criteria_restrictions = None
        
    # Get projection permissions
    try:
        projections_restrictions = cherrypy.session['_ts_user']['restrictions'][collection]['get']['projections']
    except (KeyError, TypeError):
        projections_restrictions = None

    # If there are no restrictions, check if is set to True
    if not criteria_restrictions and not projections_restrictions:
        # If collection.get is not set to True, the access is denied
        try:
            get_permissions = cherrypy.session['_ts_user']['restrictions'][collection]['get']
        except (KeyError, TypeError):
            get_permissions = None        
            
        if get_permissions != True:
            raise TSValidationError("Access to 'get.%s' is restricted for current user" % (collection))
        
        # Else, returns as allowed
        else:
            return
    
    # Validate projections and sort
    if projections_restrictions:
        restricted_field = next((p for p in projection if p in projections_restrictions), None)
        
        if not restricted_field:
            restricted_field = next((p for p in sort if p in projections_restrictions), None)
            
        if restricted_field:
            raise TSValidationError("Field 'get.%s.%s' is restricted for current user" % (collection, restricted_field))

    
    # Validate criteria
    if criteria_restrictions:
        jsonschema.validate(criteria, criteria_restrictions, format_checker=jsonschema.FormatChecker())
        
    