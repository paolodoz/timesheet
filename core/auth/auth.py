# -*- encoding: UTF-8 -*-
#
# Form based authentication for CherryPy. Requires the
# Session tool to be loaded.
#

import cherrypy, logging, pprint
from core.config import conf_auth, conf_auth_db, conf_auth_ldap, templates
from core.validation.permissions import get_user_restrictions
from core.api.crud import db
from core import auth

def check_credentials(username, password):
    """Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure"""
    
    # Try login with core/auth_*.py functions specified in config.yaml auth section
    auth_providers = conf_auth['providers']    
    for provider in auth_providers:
        auth_module = __import__('core.auth.auth_%s' % provider, fromlist=["*"])
        
        try:
            auth_error = auth_module.check_credentials(username, password)
        except Exception as e:
            auth_error = str(e)
            
        if not auth_error:
            break
        
    return auth_error
    
def check_active_status(username):
    user_record = db.user.find({ 'username' : username }, { 'status' : 1, '_id' : 0}).limit(1)
    if user_record: 
        user_status = user_record[0].get('status')
        print 'NDEEE', user_status
        if user_status == 'active':
            return
        
    return u"User not active."


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
        user_record = db.user.find({ 'username' : cherrypy.request.login }, { 'group' : 1, '_id' : 0}).limit(1)
        if user_record: 
            user_group = user_record[0].get('group')
            return user_group == 'administrator' or user_group == groupname
        
    return check

def is_logged():
    return lambda: bool(cherrypy.request.login)

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



def _unique_keeping_order(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

# Controller to provide login and logout actions
class AuthController(object):
    
    def reload_users_projects(self):

        # Save ids of managed_projects
        cherrypy.session['_ts_user']['managed_projects'] = []
        cursor = db.project.find({ 'responsibles._id' : cherrypy.session['_ts_user']['_id'] }, { '_id' : 1 })
        for document in cursor:
            cherrypy.session['_ts_user']['managed_projects'].append(str(document['_id']))

        # Save ids of taken projects
        cherrypy.session['_ts_user']['employed_projects'] = []
        cursor = db.project.find({ 'employees._id' : cherrypy.session['_ts_user']['_id'] }, { '_id' : 1 })
        for document in cursor:
            cherrypy.session['_ts_user']['employed_projects'].append(str(document['_id']))

        # Uniq and ordered ids of all projects
        cherrypy.session['_ts_user']['projects'] = _unique_keeping_order(cherrypy.session['_ts_user']['employed_projects'] +
                                                                        cherrypy.session['_ts_user']['managed_projects'])

        # Save formatted permissions schemas to speedup following accesses
        cherrypy.session['_ts_user']['restrictions'] = get_user_restrictions()

        cherrypy.log('%s' % (pprint.pformat(cherrypy.session['_ts_user'])), context = 'TS.AUTH.session_permission', severity = logging.INFO)

    def on_login(self, username):
        """Called on successful login"""
        
        # Save user data
        cherrypy.session['_ts_user'] = db.user.find_one({ 'username' : username }, { 'username' : 1, 'group' : 1, 'name' : 1, 'surname' : 1, 'email' : 1 })
        
        self.reload_users_projects()

        cherrypy.request.login = username
        
    def on_logout(self, username):
        """Called on logout"""
        cherrypy.lib.sessions.expire()
    
    def get_loginform(self, username, msg="", from_page="/"):
        return templates.get_template('auth.tpl').render(message=msg)
        
    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/"):
        if username is None or password is None:
            return self.get_loginform("", from_page=from_page)
        
        error_msg = check_credentials(username, password)
        if not error_msg:
            error_msg = check_active_status(username)
        
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