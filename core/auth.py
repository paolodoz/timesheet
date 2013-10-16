# -*- encoding: UTF-8 -*-
#
# Form based authentication for CherryPy. Requires the
# Session tool to be loaded.
#

import cherrypy
from core.config import conf_auth, conf_auth_db, conf_auth_ldap, templates
from core.permissions import get_formatted_restrictions
from core.db import db


def check_credentials(username, password):
    """Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure"""
    
    # Try login with core/auth_*.py functions specified in config.yaml auth section
    auth_providers = conf_auth['providers']    
    for provider in auth_providers:
        auth_module_package = __import__('core.auth_%s' % provider)
        auth_module = getattr(auth_module_package, 'auth_%s' % provider)
        
        try:
            auth_error = auth_module.check_credentials(username, password)
        except Exception as e:
            auth_error = str(e)
            
        if not auth_error:
            break
        
    return auth_error
    


def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        userdata = cherrypy.session.get('_ts_user')
        if userdata:
            username = userdata.get('username')
            if username:
                cherrypy.request.login = username
                for condition in conditions:
                    # A condition is just a callable that returns true or false
                    if not condition():
                        raise cherrypy.HTTPRedirect("/auth/login")
        else:
            raise cherrypy.HTTPRedirect("/auth/login")
    
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate


# Conditions are callables that return True
# if the user fulfills the conditions they define, False otherwise
#
# They can access the current username as cherrypy.request.login
#
# Define those at will however suits the application.

def member_of(groupname):
    def check():
        
        user_record = db['user'].find_one({ 'username' : cherrypy.request.login })
        if user_record:
            user_group = user_record.get('group', None)
            if user_group:
                return user_group == 'administrator' or user_group == groupname
    return check

def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.request.login

# These might be handy

def any_of(*conditions):
    """Returns True if any of the conditions match"""
    def check():
        for c in conditions:
            if c():
                return True
        return False
    return check

# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
    """Returns True if all of the conditions match"""
    def check():
        for c in conditions:
            if not c():
                return False
        return True
    return check


# Controller to provide login and logout actions

class AuthController(object):
    
    def on_login(self, username):
        """Called on successful login"""
        
        # Save user data
        cherrypy.session['_ts_user'] = db['user'].find_one({ 'username' : username }, { 'username' : 1, 'group' : 1 })
        
        # Save formatted permissions schemas to speedup following accesses
        cherrypy.session['_ts_user']['restrictions'] = get_formatted_restrictions()
        
        cherrypy.request.login = username
        
    def on_logout(self, username):
        """Called on logout"""
    
    def get_loginform(self, username, msg="", from_page="/"):
        return templates.get_template('auth.tpl').render(message=msg)
        
    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/"):
        if username is None or password is None:
            return self.get_loginform("", from_page=from_page)
        
        error_msg = check_credentials(username, password)
        if error_msg:
            return self.get_loginform(username, error_msg, from_page)
        else:
            self.on_login(username)
            raise cherrypy.HTTPRedirect(from_page or "/")
    
    @cherrypy.expose
    def logout(self, from_page="/"):
        sess = cherrypy.session
        userdata = sess.get('_ts_user', None)
        username = userdata.get('username', None)
        sess['_ts_user'] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or "/")