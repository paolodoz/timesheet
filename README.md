Abinsula Timesheet
=========

Setup
-----


  1. Install Python package installer and some libraries

        sudo apt-get install python-dev python-pip libldap2-dev libsasl2-dev

  2. Install the main dependencies

        sudo pip install --upgrade PyYAML pymongo mako jsonschema python-ldap pyOpenSSL

  3. Install and run [mongodb](http://docs.mongodb.org/manual/installation/) database

  4. Run setup script to check installation and add first administrator user

        ./setup.py --add-user <username> <password> administrator

  5. If required, customize the configuration file _core/config.yaml_.

  6. Timesheet can be run as standalone web server or embedded with apache mod_wsgi. To run it as standalone service, execute

        ./timesheet.py

  7. Point your browser to the web interface, by default: [https://localhost:9090](https://localhost:9090)
  
  8. Make profits :)

Technology references
-----

  1. Cherrypy (http://www.cherrypy.org/)

  2. Bootstrap (http://getbootstrap.com/)

  3. Fullcalendar (http://arshaw.com/fullcalendar/)

  4. jqPlot (http://www.jqplot.com/)

  5. jQuery (http://jquery.com/)

  6. JSON2 (https://github.com/douglascrockford/JSON-js)

  7. jQuery validation (http://jqueryvalidation.org/)

  8. jQuery colorpicker (https://github.com/paolodoz/really-simple-bootstrap-color-picker)

  9. Bootstrap datepicker (https://github.com/eternicode/bootstrap-datepicker)

  10. Bootstrap slider (https://github.com/seiyria/bootstrap-slider)

  11. Bootstrap switch (https://github.com/nostalgiaz/bootstrap-switch)

