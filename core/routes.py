import cherrypy, os, traceback
from core.auth import AuthController, require, member_of
from core import db
from config import views_folder, templates
from glob import glob


# Set available views dictionary
views = {}
for view_path in glob(os.path.join(views_folder, '*.html')):
    views[os.path.splitext(os.path.basename(view_path))[0]] = view_path

class Routes:
    
    # Set authorization controller options
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True,
        'tools.sessions.name' : 'name'
    }
    auth = AuthController()
    
    @cherrypy.expose
    @require(member_of("employee"))
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
    @require(member_of("employee"))
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
    @require(member_of("employee"))
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
        except Exception as e:
            #import traceback; traceback.print_exc()
            return {'error' : '%s: %s' % (type(e).__name__, str(e)), 'records' : []}
        else:
            return { 'error' : None, 'records' : records}
     
    @cherrypy.expose
    @require(member_of("employee"))
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
        except Exception as e:
            return {'error' : '%s: %s' % (type(e).__name__, str(e)) }
        else:
            return { 'error' : None }
            
    @cherrypy.expose
    @require(member_of("employee"))
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
            return {'error' : '%s: %s' % (type(e).__name__, str(e)) }
        else:
            return { 'error' : None }  