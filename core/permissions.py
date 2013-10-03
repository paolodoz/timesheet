import yaml, cherrypy
from validictory import ValidationError
from validation import recursive_replace
from config import criteria_restrictions_schema, denied_requests_schema

def get_formatted_permissions():
    """Format restriction schemas. Saved on auth login to speedup following accesses"""
    
    # Recursively replace needs a condition_function and replace_function
    replacements = { '%%username%%' : cherrypy.session['_ts_user']['username'], '%%_id%%' : cherrypy.session['_ts_user']['_id'] }
    replacements_templates = replacements.keys()

    def _replace_function_permissions_schema(container):
        if isinstance(container,basestring) and container in replacements_templates:
            return str(replacements[container])

    return {
            'group_criteria_restrictions' : recursive_replace(criteria_restrictions_schema.get(cherrypy.session['_ts_user']['group'], {}),
                                                              _replace_function_permissions_schema),
            'group_denied_requests' : denied_requests_schema.get(cherrypy.session['_ts_user']['group'], {})
            }

def restrict_criteria(action, collection, criteria):    
    """Restrict user criteria restrictions"""
    
    group_criteria_restrictions = cherrypy.session['_ts_user']['group_criteria_restrictions']
    
    try:
        # Check if request restrictions are set for the user.collection 
        restrictions = group_criteria_restrictions[collection]
    except KeyError:
        # If not, skip procedure
        pass
    else:
        # Else, check if records are accessible using group_criteria_restrictions schema formatted with current user data
        
        # If some of the restrictions are already set in criteria with different values, raise an error 
        for restr_k, restr_v in restrictions.items():
            if restr_k in criteria and criteria[restr_k] != restr_v:
                raise ValidationError("Value '%s' is restricted to user value" % (restr_k))
            
        criteria.update(restrictions)
            
    return criteria
    
    

def check_request_permissions(action, collection, projections = {}):    
    """Check if group user can access to the resource"""
    
    group_denied_requests = cherrypy.session['_ts_user']['group_denied_requests']
    
    try:
        # Raise an error if group or group.action or group.action.collection is set to false
        if group_denied_requests == False or group_denied_requests[action] == False or group_denied_requests[action][collection] == False:
            raise ValidationError("%s %s restricted for users in group '%s'" % (action, collection, cherrypy.session['_ts_user']['group']))
        
        # Raise an error if any of group.action.collection.field is set to false
        for field in [field for field,v in projections.items() if v == 1]:
            if group_denied_requests[action][collection][field] == False:
                raise ValidationError("%s %s.%s restricted for users in group '%s'" % (action, collection, field, cherrypy.session['_ts_user']['group']))
        
    
    except KeyError:
        pass
    
        
        
    
    
       