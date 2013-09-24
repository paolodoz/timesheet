#!/usr/bin/env python

import sys
from core.config import conf_auth_db, version
from core.validation import calculate_password_and_salt

print '[+] Welcome to Abinsula Timesheet version %s\n' % (version)
print '[+] Checking libraries.. ',

libraries = { 
           'cherrypy' : 'Missing some cherrypy dependencies',
           'yaml' : "Missing 'python-yaml' ptyhon package", 
           'pymongo' : "Missing 'pymongo' ptyhon package", 
           'bson' : "Missing 'python-bson' python package",
           'mako' : "Missing 'python-mako' python package",
           }

for lib, message in libraries.items():
    try: 
        __import__(lib)
    except ImportError as e:
        sys.exit(message)


print 'OK!\n[+] Checking mongodb connection.. ',

try:
    from pymongo import MongoClient as Connection
except ImportError, e:
    try:
        from pymongo import Connection
    except ImportError, e:
        sys.exit('Error importing pymongo connection object')

from core.config import collections, conf_mongodb

try:
    connection = Connection(conf_mongodb['hostname'], conf_mongodb['port'])
except Exception, e:
    sys.exit('Error connecting to database, please check if mongodb is running %s:%i or change core/config.yaml configuration.' % (conf_mongodb['hostname'], conf_mongodb['port']))    

if len(sys.argv)>1 and sys.argv[1] == '--drop':
    print 'OK!\n[+] Dropping database.. ',
    connection.drop_database(conf_mongodb['db'])
else:
    print 'OK!\n[-] Skipping database drop, run with --drop argument to reset the database',

db = connection[conf_mongodb['db']]

# Create on database missing collections names
for missing_collection in (set(collections) - set(db.collection_names())):
    db[missing_collection]

print 'OK!\n[+] Adding administrator credential in \'user\' collection with %s:%s.. ' % (conf_auth_db['init.default.admin'], conf_auth_db['init.default.password']),

password_and_salt = calculate_password_and_salt(conf_auth_db['init.default.password'])

db['user'].update( { '_id' : 1 }, dict({ '_id' : 1, 'name' : 'Admin', 'surname' : 'Default', 'username': conf_auth_db['init.default.admin'], 'email' : 'admin@localhost', 'phone' : '', 'mobile' : '', 'city' : '', 'group' : 'administrator'  }, **password_and_salt), True)
    
