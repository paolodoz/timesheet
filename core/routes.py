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
    
    @cherrypy.expose
    @require(member_of("users"))
    def index(self, view = 'index'):
        """
        Serves HTML views stored in 'views/<view>.html' rendered with template 'templates/index.tpl'
        
        GET /index/<view>
        """
        
        if view in views.keys():
            return templates.get_template('index.tpl').render(view=open(views[view]).read())
        else:
            raise cherrypy.HTTPError(404)
        

    @cherrypy.expose
    @require(member_of("users"))
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
        except Exception as e:
            return {'error' : '%s: %s' % (type(e).__name__, str(e)), 'ids' : []}
        else:
            return { 'error' : None, 'ids' : ids }
        

    @cherrypy.expose
    @require(member_of("users"))
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def get(self, collection):
        """
        Get elements list. 
        
        GET /get/<collection>/
        
        Expects a JSON filter { 'fk1' : 'fv1', 'fk2' : 'fv2', .. }
        Returns { 'error' : string, 'records' : [ {}, {}, .. ]  } 
        """
        
        json_in = cherrypy.request.json 
        try:
            records = db.get(collection, json_in)
        except Exception as e:
            return {'error' : '%s: %s' % (type(e).__name__, str(e)), 'records' : []}
        else:
            return { 'error' : None, 'records' : records}
     
    @cherrypy.expose
    @require(member_of("users"))
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def remove(self, collection):
        """
        Remove elements. 
        
        POST /remove/<collection>/
        
        Expects a list of JSON filter [ { 'fk1' : 'fv1' }, { 'fk2' : 'fv2' } ]
        Returns { 'error' : string }
        """

        json_in = cherrypy.request.json 
        try:
            ids = db.remove(collection, json_in)
        except Exception as e:
            return {'error' : '%s: %s' % (type(e).__name__, str(e)) }
        else:
            return { 'error' : None }
            
    @cherrypy.expose
    @require(member_of("users"))
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
            ids = db.update(collection, json_in)
        except Exception as e:
            raise
            return {'error' : '%s: %s' % (type(e).__name__, str(e)) }
        else:
            return { 'error' : None }  