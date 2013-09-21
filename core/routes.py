import cherrypy, os
from core.auth import AuthController, require, member_of
from mako.lookup import TemplateLookup
from config import templates_folder, views_folder
from glob import glob

    
# Set template engine
templates = TemplateLookup(directories=[templates_folder])

# Set available views dictionary
views = {}
for view_path in glob(os.path.join(views_folder, '*.html')):
    views[os.path.splitext(os.path.basename(view_path))[0]] = view_path
print views

class Routes:
    
    # Set authorization controller options
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True,
    }
    auth = AuthController()
    
    # Serve views stored in 'views/<view>.html' rendered with 
    # template 'templates/index.tpl'
    #
    # Get /index/<view> to get view
    
    @cherrypy.expose
    @require(member_of("users"))
    def index(self, view = 'index'):
        
        if view in views.keys():
            return templates.get_template('index.tpl').render(view=open(views[view]).read())
        else:
            raise cherrypy.HTTPError(404)
        

#     # Add new customers POST
#     @cherrypy.expose
#     @cherrypy.tools.allow(methods=['POST'])
#     @require(member_of("users"))
#     def customer(self):
#         pass
        