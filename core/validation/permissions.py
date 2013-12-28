import yaml, cherrypy, types, jsonschema, logging
from core.validation.validation import TSValidationError, recursive_replace, ObjectId
from core.config import restrictions_schema, conf_approval_flow
from jsonschema.exceptions import SchemaError
from core.validation.jsonschemafix import validator

def get_role_approval_step(group):

    # Approvation roles 
    approvation_roles = [ s['approver'] if 'approver' in s else '' for s in conf_approval_flow ]

    # Administrator can see every expence, return 0
    if group == 'administrator':
        return 0
    # Roles that can approves can see only expences >= owned step.
    elif group in approvation_roles[1:-1]:
        return approvation_roles.index(group)
    # Else, return draft step 
    else:
        return len(approvation_roles)-1
    

def get_user_restrictions():
    """Format restriction schemas. Saved on auth login to speedup following accesses"""
    
    
    # Recursively replace needs a condition_function and replace_function
    replacements = { 
                    '%%username%%' : '^%s$' % (cherrypy.session['_ts_user']['username']), 
                    '%%_id%%' : '^%s$' % (str(cherrypy.session['_ts_user']['_id'])),
                    '%%managed_projects%%' : (cherrypy.session['_ts_user']['managed_projects']),
                    '%%employed_projects%%' : (cherrypy.session['_ts_user']['employed_projects']),
                    '%%projects%%' : (cherrypy.session['_ts_user']['projects']),
                    '%%approval_flow%%' : get_role_approval_step(cherrypy.session['_ts_user']['group']),
                    '%%draft_flow%%' : get_role_approval_step('draft'),
                    }

    def _replace_function_permissions_schema(container):
        if isinstance(container,basestring):
            replacement = replacements.get(container)
            if replacement != None:
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
    
    try:
        restrictions = cherrypy.session['_ts_user']['restrictions'][action]
    except (KeyError, TypeError):
        restrictions = None
        
    if not restrictions:
        raise TSValidationError("Access to '%s' is restricted for current user" % (action))
    elif restrictions != True:
        validator(restrictions, format_checker=jsonschema.FormatChecker()).validate(document)

    
    
def check_remove_permissions(collection, document):
    
    # Get remove permissions
    try:
        restrictions = cherrypy.session['_ts_user']['restrictions'][collection]['remove']
    except (KeyError, TypeError):
        restrictions = None
        
    if not restrictions:
        raise TSValidationError("Access to 'remove.%s' is restricted for current user" % (collection))
    elif restrictions != True:       
        validator(restrictions, format_checker=jsonschema.FormatChecker()).validate(document)
    
def check_upsert_permissions(action, collection, document):
    
    # Get add/update permissions
    try:
        restrictions = cherrypy.session['_ts_user']['restrictions'][collection][action]
    except (KeyError, TypeError):
        restrictions = None
        
    if not restrictions:
        raise TSValidationError("Access to '%s.%s' is restricted for current user" % (action, collection))
    elif restrictions != True:       
        validator(restrictions, format_checker=jsonschema.FormatChecker()).validate(document)

def check_get_permissions(collection, criteria, projection, sort):

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
        validator(criteria_restrictions, format_checker=jsonschema.FormatChecker()).validate(criteria)
        
    