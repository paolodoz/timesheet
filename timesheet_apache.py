#!/usr/bin/env python

import cherrypy, logging
import sys, os

installation_path = os.path.dirname(__file__)

sys.path.insert(0, installation_path)
from core.routes.routes import Routes
from core.config import conf_server, conf_static, conf_logging

def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"

# Update configurations
cherrypy.config.update(conf_server)
cherrypy.config.update({'environment': 'embedded'})

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
