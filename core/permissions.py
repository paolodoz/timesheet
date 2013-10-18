import yaml, cherrypy
from validation import TSValidationError, recursive_replace
from config import restrictions_schema

def get_formatted_restrictions():
    """Format restriction schemas. Saved on auth login to speedup following accesses"""
    
    # Recursively replace needs a condition_function and replace_function
    replacements = { 
                    '%%username%%' : cherrypy.session['_ts_user']['username'], 
                    '%%_id%%' : cherrypy.session['_ts_user']['_id'],
                    '%%managed_projects%%' : cherrypy.session['_ts_user']['managed_projects'] 
                    }
    replacements_templates = replacements.keys()

    def _replace_function_permissions_schema(container):
        if isinstance(container,basestring) and container in replacements_templates:
            return str(replacements[container])

    return recursive_replace(restrictions_schema, _replace_function_permissions_schema)

def restrict_criteria(action, collection, criteria):    
    """Restrict user criteria restrictions"""
    
    group = cherrypy.session['_ts_user']['group']
    
    try:
        # Check if request restrictions are set for the collection.user
        restrictions = cherrypy.session['_ts_user']['restrictions'][collection]['criteria_restrictions'][group]
    except KeyError:
        # If not, skip procedure
        return criteria
    
    # Else, check if records are accessible using user_restrictions schema formatted with current user data
    
    # If some of the restrictions are already set in criteria with different values, raise an error 
    for restr_k, restr_v in restrictions.items():
        if restr_k in criteria and criteria[restr_k] != restr_v:
            raise TSValidationError("Field '%s' is restricted for current user" % (restr_k))
        
    criteria.update(restrictions)
        
    return criteria
    
    

def check_request_permissions(action, collection, projections = {}):    
    """Check if group user can access to the resource"""
    
    group = cherrypy.session['_ts_user']['group']
    
    try:
        # Check if request restrictions are set for the collection.user
        restrictions_projs = cherrypy.session['_ts_user']['restrictions'][collection]['projection_restrictions'][group]
    except KeyError:
        # If not, skip procedure
        pass
    else:
        # If some projection is restricted, raise an error 
        restricted_projs = next((p for p in projections if p in restrictions_projs), None)
        if restricted_projs:
            raise TSValidationError("Field '%s' is restricted for current user" % (restricted_projs))
        
    try:
        # Check if request restrictions are set for the collection.user
        restrictions_acts = cherrypy.session['_ts_user']['restrictions'][collection]['action_restrictions'][group]

        if action in restrictions_acts:
            raise TSValidationError("Action '%s' in '%s' is restricted for current user" % (action, collection))
        
    except KeyError:
        # If not, skip procedure
        pass
        
        
    
    
       