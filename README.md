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

