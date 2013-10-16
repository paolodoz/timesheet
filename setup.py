#!/usr/bin/env python

import sys
from core.config import conf_auth_db, version, collections, conf_mongodb, conf_auth_ldap
from core.validation import update_password_salt_user_json, sanitize_objectify_json
from core.auth_ldap import check_credentials
from pymongo import ASCENDING

def _check_libs():
    
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
        

def _check_ldap():
    
    if '--ldap' in sys.argv and len(sys.argv) > sys.argv.index('--ldap') + 2:
        print 'OK!\n[+] Testing LDAP username authentication..',
        arg_index = sys.argv.index('--ldap')
        username = sys.argv[arg_index+1]
        password = sys.argv[arg_index+2]
        
        print '\nHost: %s\nBind and search string: %s\nFiter: %s\nPassword: %s' % (
                                                               conf_auth_ldap['hostname'],
                                                               conf_auth_ldap['bind_search_string'].format(username=username),
                                                               conf_auth_ldap['search_filter'].format(username=username),
                                                               password
                                                               )
        
        auth_err = None
        try:
            auth_err = check_credentials(username, password, migrate=False)
        except Exception as e:
            auth_err = str(e)

        if auth_err:
           sys.exit('LDAP check credential error: %s' % (auth_err)) 
        
        
    else:
        print 'OK!\n[-] Skipping LDAP test, run with --ldap <username> <password> to check LDAP username authentication',

        
def _check_mongodb():
        
    print 'OK!\n[+] Checking mongodb connection.. ',
    
    try:
        from pymongo import MongoClient as Connection
    except ImportError, e:
        try:
            from pymongo import Connection
        except ImportError, e:
            sys.exit('Error importing pymongo connection object')
    
    
    try:
        connection = Connection(conf_mongodb['hostname'], conf_mongodb['port'])
    except Exception, e:
        sys.exit('Error connecting to database, please check if mongodb is running %s:%i or change core/config.yaml configuration.' % (conf_mongodb['hostname'], conf_mongodb['port']))    

    return connection

def _drop_db(connection):
    if len(sys.argv)>1 and sys.argv[1] == '--drop':
        print 'OK!\n[+] Dropping database.. ',
        connection.drop_database(conf_mongodb['db'])
    else:
        print 'OK!\n[-] Skipping database drop, run with --drop argument to reset the database',

def _create_db_collections(connection):
    db = connection[conf_mongodb['db']]
    
    # Create on database missing collections names
    for missing_collection in (set(collections) - set(db.collection_names())):
        db[missing_collection]

    # Set unique parameters
    db['user'].ensure_index( 'username', unique = True )
    db['day'].ensure_index( 'date', unique = True )
    
    return db

def _add_default_admin(db):
    
    if '--add-admin-ldap' in sys.argv and '--ldap' in sys.argv and len(sys.argv) > sys.argv.index('--ldap') + 2:
        arg_index = sys.argv.index('--ldap')
        username = sys.argv[arg_index+1]
        password = sys.argv[arg_index+2]
        print 'OK!\n[+] Adding administrator credentials ' + username + ' for LDAP auth',
        
        auth_err = None
        try:
            auth_err = check_credentials(username, password, migrate=True, group_on_migration='administrator')
        except Exception as e:
            auth_err = str(e)
        
    elif '--add-admin' in sys.argv and len(sys.argv) > sys.argv.index('--add-admin') + 2:
        arg_index = sys.argv.index('--add-admin')
        username = sys.argv[arg_index+1]
        password = sys.argv[arg_index+2]
        print 'OK!\n[+] Adding administrator credentials ' + username + ':' + password,
    
        json_user = { '_id' : '1'*24, 'password' : password, 'name' : 'Admin', 'surname' : 'Default', 'username': username, 'email' : 'admin@localhost', 'phone' : '', 'mobile' : '', 'city' : '', 'group' : 'administrator', 'salary' : []  }
    
        sanified_documents_list = sanitize_objectify_json(json_user)
        update_password_salt_user_json(sanified_documents_list)
        
        db['user'].update( { '_id' : '1'*24 }, sanified_documents_list, True)
    else:
        print 'OK!\n[-] Skipping admin insert, use \'--add-admin <usr> <pwd>\' or \'--ldap <usr> <pwd> --add-admin-ldap\''

if __name__ == "__main__":
    
    print '[+] Abinsula Timesheet version %s install script' % (version)
    
    _check_libs()
    connection = _check_mongodb()
    _drop_db(connection)
    db = _create_db_collections(connection)
    _check_ldap()
    _add_default_admin(db)

