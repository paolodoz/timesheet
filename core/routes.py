import cherrypy, os, traceback
from core.auth import AuthController, require, member_of
from core import dbm
from mako.lookup import TemplateLookup
from config import templates_folder, views_folder
from glob import glob

    
# Set template engine
templates = TemplateLookup(directories=[templates_folder])

# Set available views dictionary
views = {}
for view_path in glob(os.path.join(views_folder, '*.html')):
    views[os.path.splitext(os.path.basename(view_path))[0]] = view_path

class Routes:
    
    # Set authorization controller options
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True,
    }
    auth = AuthController()
    
    
    # Serves HTML views stored in 'views/<view>.html' rendered with 
    # template 'templates/index.tpl'
    #
    # GET /index/<view>
    
    @cherrypy.expose
    @require(member_of("users"))
    def index(self, view = 'index'):
        
        if view in views.keys():
            return templates.get_template('index.tpl').render(view=open(views[view]).read())
        else:
            raise cherrypy.HTTPError(404)
        

    # Add new elements.
    
    # POST /add/<collection>/ 
    # Expects a list of JSON defined by core/schema.yaml
    # Returns { 'error' : string, 'ids' : []  }
    
    @cherrypy.expose
    @require(member_of("users"))
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def add(self, collection):
        json_in = cherrypy.request.json 
        try:
            ids = dbm.add(collection, json_in)
        except Exception as e:
            return {'error' : '%s: %s' % (type(e).__name__, str(e)), 'ids' : []}
        else:
            return { 'error' : None, 'ids' : ids }
        
    # Get elements list. 
    
    # POST /get/<collection>/
    # Expects a JSON filter defined by schema
    # Returns { 'error' : string, 'records' : [ {}, {}, .. ]  } 
    
    @cherrypy.expose
    @require(member_of("users"))
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def get(self, collection):
        json_in = cherrypy.request.json 
        try:
            records = dbm.get(collection, json_in)
        except Exception as e:
            return {'error' : '%s: %s' % (type(e).__name__, str(e)), 'records' : []}
        else:
            return { 'error' : None, 'records' : records}
    
    
    # Remove elements. 
    
    # POST /remove/<collection>/
    # Expects a list of JSON defined by core/schema.yaml
    # Returns { 'error' : string }
    
    @cherrypy.expose
    @require(member_of("users"))
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def remove(self, collection):
        json_in = cherrypy.request.json 
        try:
            ids = dbm.remove(collection, json_in)
        except Exception as e:
            return {'error' : '%s: %s' % (type(e).__name__, str(e)) }
        else:
            return { 'error' : None }
            
        