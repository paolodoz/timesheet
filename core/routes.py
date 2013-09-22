import cherrypy, os
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
    # GET /index/<view> -> HTML
    
    @cherrypy.expose
    @require(member_of("users"))
    def index(self, view = 'index'):
        
        if view in views.keys():
            return templates.get_template('index.tpl').render(view=open(views[view]).read())
        else:
            raise cherrypy.HTTPError(404)
        

    # Add new element. Admin session required. Expects and respond JSON.
    # POST /add/<document>/ <- json -> json
    @cherrypy.expose
    @require(member_of("users"))
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def add(self, document):
        json = cherrypy.request.json 
        try:
            db.add(document, json)
        except Exception as e:
            return self._format_err(e)
        
    # Get elements. Admin session required. Expects and respond JSON.
    # POST /get/<document>/ <- json -> json
    @cherrypy.expose
    @require(member_of("users"))
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def get(self, document):
        json = cherrypy.request.json 
        try:
            return db.get(document, json)
        except Exception as e:
            return self._format_err(e)
    
    
    # Format returning json in case of errors 
    def _format_err(self, e):
        json = {'error' : '%s: %s' % (type(e).__name__, str(e))}
        print json
        return json