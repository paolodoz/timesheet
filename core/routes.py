import cherrypy, os, traceback
from core.auth import AuthController, require, member_of
from core import db
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
        

    # Add new element.
    
    # POST /add/<document>/ 
    # Expects a JSON defined by schema
    # Returns { 'error' : string, '_id' : string  }
    
    @cherrypy.expose
    @require(member_of("users"))
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def add(self, collection):
        json_in = cherrypy.request.json 
        try:
            id = db.add(collection, json_in)
        except Exception as e:
            return {'error' : '%s: %s' % (type(e).__name__, str(e)), '_id' : -1}
        else:
            return { 'error' : None, '_id' : id }
        
    # Get an elements list. 
    
    # POST /get/<document>/
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
            records = db.get(collection, json_in)
            return { 'error' : None, 'records' : records}
        except Exception as e:
            return {'error' : '%s: %s' % (type(e).__name__, str(e)), 'records' : []}
    
    
    # Remove an element. 
    
    # POST /remove/<document>/
    # Expects a JSON filter defined by schema
    # Returns { 'error' : string  } 
    
    @cherrypy.expose
    @require(member_of("users"))
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def remove(self, collection):
        json_in = cherrypy.request.json 
        try:
            db.remove(collection, json_in)
            return { 'error' : None, }
        except Exception as e:
            return {'error' : '%s: %s' % (type(e).__name__, str(e)) }
        