#!/usr/bin/env python

import cherrypy, logging
from core.routes.routes import Routes
from core.config import conf_server, conf_static, conf_logging

def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"


if __name__ == '__main__':
    
    # Update configurations
    cherrypy.config.update(conf_server)
    cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders, priority=60)
    
    for logname, loglevel in conf_logging.items():
        logging_level = getattr(logging, loglevel)
        cherrypy_log = getattr(cherrypy.log, logname)
        cherrypy_log.setLevel(logging_level)
    
    routes = Routes()
    
    cherrypy.quickstart(routes, '/', config=conf_static)
