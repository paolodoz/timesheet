from core.api import datamine
from jsonschema.exceptions import ValidationError
from core.validation.validation import TSValidationError
from core.auth.auth import AuthController, require, is_logged
import cherrypy, traceback, logging, cgi

class DatamineRoutes:
    
    @cherrypy.expose
    @require(is_logged())
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in(on = True)
    @cherrypy.tools.json_out(on = True)
    def default(self, action):
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
            json_out = {'error' : '%s: %s' % (type(e).__name__, cgi.escape(e.message)) }
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, cgi.escape(str(e))) }
        except Exception as e:
            error_msg = '%s %s\n%s %s\n' % (str(json_in), type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s internal exception' % (type(e).__name__) }       
        else:
            error_msg = None
            json_out = dict({ 'error' : None }, **returned_dict)
        
        if error_msg:
            cherrypy.log('%s %s' % (cherrypy.request.path_info, error_msg), context = 'TS', severity = logging.ERROR)
        
        return json_out

