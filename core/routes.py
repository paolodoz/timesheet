import cherrypy, os
from core.auth import AuthController, require, member_of
from config import www_folder


class Routes:
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True,
    }
    
    auth = AuthController()
    
    @cherrypy.expose
    @require(member_of("users"))
    def index(self, **keywords):
        return open(os.path.join(www_folder, 'main.html'))
        
