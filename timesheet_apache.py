#!/usr/bin/env python

import cherrypy, logging
import sys, os

# Suppose this file in 
installation_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

sys.path.insert(0, installation_path)
from core.routes.routes import Routes
from core.config import conf_server, conf_static, conf_logging

def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"

# Update configurations
# If log paths are absolute, move to current path
if not os.path.isabs(conf_server['log.access_file']):
    conf_server['log.access_file'] = os.path.join(installation_path, conf_server['log.access_file'])
if not os.path.isabs(conf_server['log.error_file']):
    conf_server['log.error_file'] = os.path.join(installation_path, conf_server['log.error_file'])
    
conf_server['environment'] = 'embedded'
cherrypy.config.update(conf_server)
    

if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

for logname, loglevel in conf_logging.items():
    logging_level = getattr(logging, loglevel)
    cherrypy_log = getattr(cherrypy.log, logname)
    cherrypy_log.setLevel(logging_level)

cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders, priority=60)

routes = Routes()
application = cherrypy.Application(routes, config=conf_static)
