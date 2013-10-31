Abinsula Timesheet
=========

Setup
-----


  1. If required, install Python package installer

        sudo apt-get install pip

  2. Install the dependencies

        sudo pip install cherrypy yaml pymongo bson mako jsonschema

  3. Install and run [mongodb](http://docs.mongodb.org/manual/installation/) database

  4. Run setup script to check installation and add first administrator user

        ./setup.py --add-user <username> <password> administrator

  5. If required, customize the configuration file _core/config.yaml_.

  6. Point your browser to the web interface, by default: [https://localhost:9090](https://localhost:9090)
  
  7. Make profits :)

