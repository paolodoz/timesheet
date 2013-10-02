import yaml, cherrypy
from validictory import ValidationError
from config import criteria_restrictions, denied_requests 


def _change_recurs_dict(d, replacements):
    new = {}
    for k, v in d.iteritems():
        if isinstance(v, dict):
            v = _change_recurs_dict(v, replacements)
        elif isinstance(v, basestring) and v in replacements:
            new[k] = v.replace(v,str(replacements[v]))
    return new

def restrict_criteria(action, collection, criteria):    
    """Restrict user criteria restrictions"""
    
    current_user_data = cherrypy.session['_ts_user']
    
    try:
        # Check if request restrictions are set for the user.collection 
        restrictions = criteria_restrictions[current_user_data['group']][collection]
    except KeyError:
        # If not, skip procedure
        pass
    else:
        # Else, get restrictions from the denied_requests.schema, replacing current user parameters
        restrictions = _change_recurs_dict(restrictions, { 
                                                '%%username%%' : current_user_data['username'],
                                                 '%%_id%%' : current_user_data['_id']
                                                }
                                          )
        
        # If some of the restrictions are already set in criteria with different values, raise an error 
        for restr_k, restr_v in restrictions.items():
            if restr_k in criteria and criteria[restr_k] != restr_v:
                raise ValidationError("Value '%s' is restricted to user value" % (restr_k))
            
        criteria.update(restrictions)
            
    return criteria
    
    

def deny_requests(action, collection, projections = {}):    
    """Check if group user can access to the resource"""
    
    current_user_group = cherrypy.session['_ts_user']['group']
    
    try:
        if denied_requests[current_user_group] == False or denied_requests[current_user_group][action] == False or denied_requests[current_user_group][action][collection] == False:
            raise ValidationError("%s %s restricted for users in group '%s'" % (action, collection, current_user_group))
        
        for field in [field for field,v in projections.items() if v == 1]:
            if denied_requests[current_user_group][action][collection][field] == False:
                raise ValidationError("%s %s.%s restricted for users in group '%s'" % (action, collection, field, current_user_group))
        
    
    except KeyError:
        pass
    
        
        
    
    
       