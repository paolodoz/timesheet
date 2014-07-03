import cherrypy, os, traceback, logging, cgi
from core.auth.auth import AuthController, require, is_logged
from core.api import crud
from core.routes.uploads import UploadsRoutes
from core.routes.datamine import DatamineRoutes
from core.config import views_folder, templates, views, conf_session, views_restrictions_schema
from core.notifications import notifications
from glob import glob
from jsonschema.exceptions import ValidationError
from core.validation.validation import TSValidationError


class Routes:
    
    # Set authorization and sessions options
    _cp_config = conf_session
    auth = AuthController()
    file = UploadsRoutes()
    data = DatamineRoutes()
    
    @cherrypy.expose
    @require(is_logged())
    def index(self, view = 'calendar'):
        """
        Serves HTML views stored in 'view/<view>.html' rendered with template 'templates/index.tpl'
        
        GET /index/<view>
        """
        
        user_views_restrictions = views_restrictions_schema.get(cherrypy.session['_ts_user']['group'], [])
        
        if view in user_views_restrictions:
            raise cherrypy.HTTPError("403 Forbidden", "You are not allowed to access this resource.")
            
        view_page = views.get_template('%s.html' % view).render(csrf_token = cherrypy.session.get('_csrf_token',''))
        return templates.get_template('index.tpl').render(view = view, view_page=view_page, user_views_restrictions=user_views_restrictions, **cherrypy.session['_ts_user'])
        
    @cherrypy.expose
    @require(is_logged())
    @cherrypy.tools.json_out(on = True)
    def me(self):
        """
        Serves a JSON with informations about logged user
        
        GET /me
        """
        
        key_list = [ 'username', 'name', 'surname', 'email', 'group']
        
        json_out = dict((key,value) for key, value in cherrypy.session['_ts_user'].iteritems() if key in key_list)
        json_out['notifications'] = notifications.get_pending()
        json_out['_id'] = str(cherrypy.session['_ts_user']['_id'])
        
        return json_out
        

    @cherrypy.expose
    @require(is_logged())
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def add(self, collection):
        """
        Add new elements.
        
        POST /add/<collection>/ 
        
        Expects a list of JSONs [ { }, { } ]
        Returns { 'error' : string, 'ids' : []  }
        """
        
        json_in = cherrypy.request.json 
        try:
            ids = crud.add(collection, json_in)
        except ValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, cgi.escape(e.message)), 'ids' : []}
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out =  {'error' : '%s: %s' % (type(e).__name__, cgi.escape(str(e))), 'ids' : []}
        except Exception as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s internal exception' % (type(e).__name__), 'ids' : []}            
        else:
            error_msg = None
            json_out = { 'error' : None, 'ids' : ids }
        
        if error_msg:
            cherrypy.log('%s %s' % (cherrypy.request.path_info, error_msg), context = 'TS', severity = logging.ERROR)
        
        return json_out

    @cherrypy.expose
    @require(is_logged())
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def get(self, collection):
        """
        Get elements list. 
        
        GET /get/<collection>/
        
        Expects a JSON list containing criteria and projection. Projection dict can't be empty. 
                [ { 'fk1' : 'fv1', .. }, { 'fk2' : 1 } ]
        Returns { 'error' : string, 'records' : [ {}, {}, .. ]  } 
        """
        
        json_in = cherrypy.request.json 
        
        try:
            records = crud.get(collection, json_in)
        except ValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, cgi.escape(e.message)), 'records' : []}
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, cgi.escape(str(e)), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, str(e)), 'records' : []}
        except Exception as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s internal exception' % (type(e).__name__), 'records' : []}   
        else:
            error_msg = None
            json_out = { 'error' : None, 'records' : records }
        
        if error_msg:
            cherrypy.log('%s %s' % (cherrypy.request.path_info, error_msg), context = 'TS', severity = logging.ERROR)
        
        return json_out
     
    @cherrypy.expose
    @require(is_logged())
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def remove(self, collection):
        """
        Remove elements. 
        
        POST /remove/<collection>/
        
        Expects a list of JSON criteria [ { 'fk1' : 'fv1' }, { 'fk2' : 'fv2' } ]
        Returns { 'error' : string }
        """

        json_in = cherrypy.request.json 
        try:
            ids = crud.remove(collection, json_in)
        except ValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, cgi.escape(e.message))}
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, cgi.escape(str(e))) }
        except Exception as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s internal exception' % (type(e).__name__) }   
        else:
            error_msg = None
            json_out = { 'error' : None }
        
        if error_msg:
          cherrypy.log('%s %s' % (cherrypy.request.path_info, error_msg), context = 'TS', severity = logging.ERROR)
        
        return json_out
            
    @cherrypy.expose
    @require(is_logged())
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def update(self, collection):
        """
        Update element. 
        
        POST /update/<collection>/
        
        Expects the JSON object containing the ID to update 
                { '_id' : ID, 'k1' : 'p1', 'k2' : 'p2', ..  }
        Returns { 'error' : string }
        """

        json_in = cherrypy.request.json 
        try:
            crud.update(collection, json_in)
        except ValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, cgi.escape(e.message))}
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, cgi.escape(str(e))) }
        except Exception as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s internal exception' % (type(e).__name__) }   
        else:
            error_msg = None
            json_out = { 'error' : None }

        if error_msg:
            cherrypy.log('%s %s' % (cherrypy.request.path_info, error_msg), context = 'TS', severity = logging.ERROR)
        
        return json_out
        



     