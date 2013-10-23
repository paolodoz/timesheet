import cherrypy, os, traceback, logging, sys
from core.auth import AuthController, require, is_logged
from core import db
from config import views_folder, templates, conf_session
from glob import glob
from core import datamine
from jsonschema.exceptions import ValidationError
from core.validation import TSValidationError


# Set available views dictionary
views = {}
for view_path in glob(os.path.join(views_folder, '*.html')):
    views[os.path.splitext(os.path.basename(view_path))[0]] = view_path


# Create session folder if does not exist
session_path = conf_session['tools.sessions.storage_path']
if not os.path.isdir(session_path):
    # TODO: check also folder permissions
    try:
        os.mkdir(session_path, 0700)
    except Exception as e:
        raise
        sys.exit('Can\'t create session folder \'%s\'' % (session_path))
    


class Routes:
    
    # Set authorization and sessions options
    _cp_config = conf_session
    auth = AuthController()
    
    @cherrypy.expose
    @require(is_logged())
    def index(self, view = 'index'):
        """
        Serves HTML views stored in 'views/<view>.html' rendered with template 'templates/index.tpl'
        
        GET /index/<view>
        """
        
        if view in views.keys():
            # Templatize index passing requested page and user session data 
            return templates.get_template('index.tpl').render(view = view, view_page=open(views[view]).read(), **cherrypy.session['_ts_user'])
        else:
            raise cherrypy.HTTPError(404)

    @cherrypy.expose
    @require(is_logged())
    @cherrypy.tools.json_out(on = True)
    def me(self):
        """
        Serves a JSON with informations about logged user
        
        GET /me
        """
        
        return { 'username' : cherrypy.session['_ts_user']['username'], '_id' : str(cherrypy.session['_ts_user']['_id'])}
        

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
            ids = db.add(collection, json_in)
        except ValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: Error \'%s\' is not valid' % (type(e).__name__, str(e.instance)), 'ids' : []}
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out =  {'error' : '%s: %s' % (type(e).__name__, str(e)), 'ids' : []}
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
            records = db.get(collection, json_in)
        except ValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: Error \'%s\' is not valid' % (type(e).__name__, str(e.instance)), 'records' : []}
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
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
            ids = db.remove(collection, json_in)
        except ValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: Error \'%s\' is not valid' % (type(e).__name__, str(e.instance)), 'ids' : []}
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, str(e)) }
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
            db.update(collection, json_in)
        except ValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: Error \'%s\' is not valid' % (type(e).__name__, str(e.instance)), 'ids' : []}
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, str(e)) }
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
    def data(self, action):
        """
        Datamine collections. 
        
        POST /data/<action>/
        
        Expects the JSON format as requested by the called function.
        Returns { 'error' : string, ... }
        """

        json_in = cherrypy.request.json 
        
        try:
            returned_dict = getattr(datamine, action)(json_in)
        except ValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: Error \'%s\' is not valid' % (type(e).__name__, str(e.instance)) }
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, str(e)) }
        except Exception as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s internal exception' % (type(e).__name__) }       
        else:
            error_msg = None
            json_out = dict({ 'error' : None }, **returned_dict)
        
        if error_msg:
            cherrypy.log('%s %s' % (cherrypy.request.path_info, error_msg), context = 'TS', severity = logging.ERROR)
        
        return json_out
        