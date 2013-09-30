import ldap
from core.config import conf_auth_ldap

def check_credentials(username, password):
    """User authentication based on LDAP"""
    
    bind_search_string = conf_auth_ldap['bind_search_string'].format(username=username)
    
    ldap_connection = ldap.open(conf_auth_ldap['hostname'])
    ldap_connection.protocol_version = ldap.VERSION3
    ldap_connection.simple_bind_s(bind_search_string, password)


    search_scope = ldap.SCOPE_SUBTREE
    attributes = None 
    search_filter = conf_auth_ldap['search_filter'].format(username=username)

    ldap_result_id = ldap_connection.search_s(bind_search_string, search_scope, search_filter, attributes)

    
    return u"Incorrect username or password."