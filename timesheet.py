#!/usr/bin/env python

import cherrypy
from core.routes import Routes
from core.config import conf_server, conf_static

if __name__ == '__main__':
    
    cherrypy.config.update(conf_server)

    routes = Routes()
    
    cherrypy.quickstart(routes, '/', config=conf_static)
