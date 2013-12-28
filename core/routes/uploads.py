from cherrypy.lib.static import serve_file
from core.api import uploads
from jsonschema.exceptions import ValidationError
from core.validation.validation import TSValidationError
from core.auth.auth import AuthController, require, is_logged
import cherrypy, traceback, logging, cgi

class UploadsRoutes:
    
    @cherrypy.expose
    @require(is_logged())
    def download(self, upload_id):
        """
        Download stored file by id.
        
        POST /file/download
        
        Returns file content.
        """
        
        try:
            file_path, content_type = uploads.download(upload_id)
        except Exception as e:      
            error_msg = '%s %s\n%s %s\n' % (str(''), type(e).__name__, str(e), traceback.format_exc())
        else:
            error_msg = None
        
        if error_msg:
            cherrypy.log('%s %s' % (cherrypy.request.path_info, error_msg), context = 'TS', severity = logging.ERROR)
        else:
            return serve_file(file_path, content_type=content_type)
    
    @cherrypy.expose
    @require(is_logged())
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_out(on = True)
    def upload(self, **postdata):
        """
        Upload stored files.
        
        POST /file/upload
        
        Returns { 'error' : string, 'upload_id' : string }
        """
        
        try:
            upload_id = uploads.upload()
            
        except ValidationError as e:
            error_msg = '%s %s\n%s %s\n' % ('', type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, cgi.escape(e.message)), 'upload_id' : ''}
        except TSValidationError as e:
            error_msg = '%s %s\n%s %s\n' % ('', type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s: %s' % (type(e).__name__, cgi.escape(str(e))), 'upload_id' : '' }
        except Exception as e:      
            error_msg = '%s %s\n%s %s\n' % ('', type(e).__name__, str(e), traceback.format_exc())
            json_out = {'error' : '%s internal exception' % (type(e).__name__), 'upload_id' : '' } 
        else:
            error_msg = None
            json_out = dict({ 'error' : None , 'upload_id' : upload_id })
        
        if error_msg:
            cherrypy.log('%s %s' % (cherrypy.request.path_info, error_msg), context = 'TS', severity = logging.ERROR)
        
        return json_out


    @cherrypy.expose
    @require(is_logged())
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_out(on = True)
    @cherrypy.tools.json_in(on = True)
    def remove(self):
        """
        Delete stored files.
        
        POST /file/remove
        
        Returns { 'error' : string }
        """
        
        json_in = cherrypy.request.json 
        
        try:
            uploads.remove(json_in)
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
