import yaml, cherrypy, types, jsonschema
from validation import TSValidationError, recursive_replace, ObjectId
from config import restrictions_schema

def get_user_restrictions(schema_name):
    """Format restriction schemas. Saved on auth login to speedup following accesses"""
    
    # Recursively replace needs a condition_function and replace_function
    replacements = { 
                    '%%username%%' : '^%s$' % (cherrypy.session['_ts_user']['username']), 
                    '%%_id%%' : '^%s$' % (str(cherrypy.session['_ts_user']['_id'])),
                    '%%managed_projects%%' : cherrypy.session['_ts_user']['managed_projects'] 
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
        
    formatted_schemas = {}
    
    for collection_name, collection_schema in restrictions_schema.items():
        try:
            schema = collection_schema[schema_name][cherrypy.session['_ts_user']['group']]
        except KeyError as e:
            pass
        else:
            formatted_schemas[collection_name] = recursive_replace(schema, _replace_function_permissions_schema)
            
    return formatted_schemas

    
def check_action_permissions(action, collection):

    try:
        # Check if request restrictions are set for the collection.user
        restrictions_acts = restrictions_schema[collection]['action_restrictions'][cherrypy.session['_ts_user']['group']]
    except KeyError:
        # If not, skip procedure
        return

    if action in restrictions_acts:
        raise TSValidationError("Action '%s' in '%s' is restricted for current user" % (action, collection))
    
def check_criteria_permissions(collection, criteria):

    try:
        # Check if request restrictions are set for the collection.user
        restrictions_criteria = cherrypy.session['_ts_user']['criteria_restrictions_schema'][collection]
    except KeyError:
        # If not, skip procedure
        return
    
    jsonschema.validate(criteria, restrictions_criteria, format_checker=jsonschema.FormatChecker())

   
def check_insert_permissions(collection, document):

    try:
        # Check if request restrictions are set for the collection.user
        restrictions_document = cherrypy.session['_ts_user']['insert_restrictions_schema'][collection]
    except KeyError:
        # If not, skip procedure
        return
    
    jsonschema.validate(document, restrictions_document, format_checker=jsonschema.FormatChecker())
    
def check_projection_permissions(collection, projections):    
    """Check if group user can access to the resource"""
    
    try:
        # Check if request restrictions are set for the collection.user
        restrictions_projs = restrictions_schema[collection]['projection_restrictions'][cherrypy.session['_ts_user']['group']]
    except KeyError:
        # If not, skip procedure
        return
    
    # If some projection is restricted, raise an error 
    restricted_projs = next((p for p in projections if p in restrictions_projs), None)
    if restricted_projs:
        raise TSValidationError("Field '%s' is restricted for current user" % (restricted_projs))
    

        
        
    
    
       