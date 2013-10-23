#!/usr/bin/env python

import cherrypy, logging
import sys, os

installation_path = ''

if not installation_path:
    sys.exit('Please set in \'timesheet_apache.py\' \'installation_path\' variable absolute folder path')

sys.path.insert(0, installation_path)
from core.routes import Routes
from core.config import conf_server, conf_cherry, conf_logging

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
application = cherrypy.Application(routes, config=conf_cherry)
