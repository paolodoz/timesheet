import yaml, cherrypy
from validictory import ValidationError
from validation import recursive_replace
from config import restrictions_schema

def get_formatted_restrictions():
    """Format restriction schemas. Saved on auth login to speedup following accesses"""
    
    # Recursively replace needs a condition_function and replace_function
    replacements = { '%%username%%' : cherrypy.session['_ts_user']['username'], '%%_id%%' : cherrypy.session['_ts_user']['_id'] }
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
            raise ValidationError("Field '%s' is restricted for current user" % (restr_k))
        
    criteria.update(restrictions)
        
    return criteria
    
    

def check_request_permissions(action, collection, projections = {}):    
    """Check if group user can access to the resource"""
    
    group = cherrypy.session['_ts_user']['group']
    
    try:
        # Check if request restrictions are set for the collection.user
        restrictions = cherrypy.session['_ts_user']['restrictions'][collection]['field_restrictions'][group]
            
        if restrictions == True:
            raise ValidationError("Collection '%s' is restricted for current user" % (collection))
        
    except KeyError:
        # If not, skip procedure
        pass
    else:
            
        # If some of the restrictions are already set in criteria with different values, raise an error 
        for restr_k, restr_v in restrictions.items():
            if restr_k in projections and restr_v == True:
                raise ValidationError("Field '%s' is restricted for current user" % (restr_k))
        
        
    try:
        # Check if request restrictions are set for the collection.user
        restrictions = cherrypy.session['_ts_user']['restrictions'][collection]['action_restrictions'][group]
        print 'AAAAAAAAAAAAaa'
        if restrictions == True or restrictions[action] == True:
            raise ValidationError("Action '%s' in '%s' is restricted for current user" % (action, collection))
        
    except KeyError:
        # If not, skip procedure
        pass
        
        
    
    
       