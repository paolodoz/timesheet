#!/usr/bin/env python

import cherrypy, logging
import sys, os
sys.path.insert(0, os.path.abspath(__file__))
from core.routes import Routes
from core.config import conf_server, conf_static, conf_logging

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

routes = Routes()

#cherrypy.quickstart(routes, '/', config=conf_static)
application = cherrypy.Application(routes, script_name=None, config=None)
