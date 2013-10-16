#!/usr/bin/env python
import urllib2, urllib, json, os, sys
from cookielib import CookieJar


# Possible users groups
users_groups = [ 'administrator', 'employee']


cj = CookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def _login(values):
    """Login procedure using admin_credentials"""
    cj.clear()
    data = urllib.urlencode(values)
    opener.open("https://localhost:9090/auth/login", data)
    

def _assert_page_contains(needle, check_contains=True):
    """Search needle in main page"""
    print '\nCHECK if user get \'%s\'' % (needle)
    request = urllib2.Request('https://localhost:9090/')
    page_returned = opener.open(request).read()
    
    assert (check_contains and needle in page_returned) or (not check_contains and not needle in page_returned)
    print 'OK!'    
    
def _assert(uri, json_in, json_expected):
    """Assert API request deleting cleaning out random parameter as _id"""
    
    request = urllib2.Request('https://localhost:9090/%s' % uri.lstrip('/'), data=json.dumps(json_in), headers={'Content-Type': 'application/json'})
    json_returned = json.loads(opener.open(request).read())
    json_returned_noid = json_returned.copy()
    
    # Dirty code to remove records real '_id's to simplify the comparison
    if 'records' in json_returned_noid:
        records = json_returned_noid['records']
        for rec in records:
            if '_id' in rec:
                rec['_id'] = ''
    elif 'ids' in json_returned_noid:
        json_returned_noid['ids'] = ['']*len(json_returned_noid['ids']) 
    else:
        records = [ json_returned_noid ]
    
    print '\nPOST ', uri , json_in, '\nRET ', json_returned_noid, '\nEXP ', json_expected
    assert(json_returned_noid == json_expected)
    print 'OK!'
    
    return json_returned


def main(admin_credentials):
    
    ## LOGIN
    _login(admin_credentials)
    
    ## CHECK LOGIN
    _assert_page_contains('Timesheet login', False)
    
    ## GET CURRENT INFORMATIONS
    _assert('/me', None, { 'username' : admin_credentials['username'], '_id' : '1'*24 })
    
    ## TEST BAD REQUESTS
    # Add directly json without list
    _assert('/add/wrong', { 'single': 'dict' }, {'error' : "ValidationError: List expected, not 'dict'", 'ids' : [] })
    # Add unexistant collection
    _assert('/add/wrong', [ { 'wrong': 'param' } ], {'error' : "KeyError: 'wrong'", 'ids' : [] })
    # Add user with unsupported param 
    _assert('/add/user', [ { 'wrong': 'param' } ], {'error' : 'ValidationError: Required field \'username\' is missing', 'ids' : []  })
    # Get without a valid projection
    _assert('/get/user', [ { }, { } ], { 'error': 'ValidationError: Expected list with criteria and nonempty projection', 'records' : [] })
    # Get badly formatted
    _assert('/get/user', [ { } ], { 'error': 'ValidationError: Expected list with criteria and nonempty projection', 'records' : [] })
       
    
    ## API CUSTOMER
    # Remove already unexistant customer
    _assert('/remove/customer', [ { 'name' : 'CUSTOMERTEST' } ], { 'error' : None  })
    # Add one customer (return one id)
    json_returned = _assert('/add/customer', [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTOMAIL', 'description' : 'CUSTODESC' } ], { 'error' : None, 'ids' : [ '' ] })
    # Get the inserted customer by name
    _assert('/get/customer', [ { 'name' : 'CUSTOMERTEST' }, { 'name' : 1, 'address' : 1, 'phone' : 1, 'contact_person' : 1, 'vat_number' : 1, '_id' : 1, 'website' : 1, 'city' : 1, 'country' : 1, 'postal_code' : 1, 'email' : 1, 'description' : 1 } ], { 'error': None, 'records' : [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', '_id' : '', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTOMAIL', 'description' : 'CUSTODESC'   } ] })
    # Get the inserted customer by id
    _assert('/get/customer', [ { '_id' : json_returned['ids'][0] }, { 'address' : 1 }], { 'error': None, 'records' : [ { 'address' : 'CUSTOMER STREET', '_id' : '' } ] })
    # Remove customer by id
    _assert('/remove/customer', [ { '_id' : json_returned['ids'][0] } ], { 'error' : None  })
    # Check if collection is empty
    _assert('/get/customer', [ { '_id' : json_returned['ids'][0] }, { '_id' : 1 } ], { 'error': None, 'records' : [ ] })
    
    ## API USER
    # Remove already unexistant user
    _assert('/remove/user', [ { 'name' : 'USERTEST'  } ], { 'error' : None  })
    # Add one customer (return one id)
    _assert('/add/user', [ { 'name' : 'USERTEST', 'surname' : 'SURNAME', 'username' : 'USERNAME', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [] } ], { 'error' : None, 'ids' : [ '' ] })
    # Add a double customer (UNIQ test)
    _assert('/add/user', [ { 'name' : 'USERTEST', 'surname' : 'SURNAME2', 'username' : 'USERNAME', 'email' : 'EMAIL2', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ], { 'error' : None, 'ids' : [ '' ] })
    # Get the inserted customer (is only one because UNIQ)
    _assert('/get/user', [ { 'name' : 'USERTEST' }, { 'surname' : 1, '_id' : 0 } ], { 'error': None, 'records' : [ { 'surname' : 'SURNAME'  } ] })
    # Delete the one inserted
    _assert('/remove/user', [ { 'name' : 'USERTEST'  } ], { 'error' : None })
    # Get the empty customers list
    _assert('/get/user', [ { 'name' : 'USERTEST' }, { '_id' : 1 } ], { 'error': None, 'records' : [ ] })
    # Add two elements USERTEST1 and USERTEST2
    _assert('/add/user', [ { 'name' : 'USERTEST1', 'surname' : 'SURNAME', 'username' : 'USERNAME1' , 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : []  }, { 'name' : 'USERTEST2', 'surname' : 'SURNAME', 'username' : 'USERNAME2' , 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : []  } ], { 'error' : None, 'ids' : [ '', '' ] })
    # Delete USERTEST1
    _assert('/remove/user', [ { 'name' : 'USERTEST1'  }, { 'name' : 'USERTEST2'  } ], { 'error' : None })
    # Check if USERTEST1 is deleted
    _assert('/get/user', [ { 'name' : 'USERTEST1' }, { '_id' : 1 } ], { 'error': None, 'records' : [ ] })

    ## API PROJECTS
    # Remove already unexistant project
    _assert('/remove/project', [ { 'name' : 'PROJECTNAME'  } ], { 'error' : None  })
    # Add one project
    _assert('/add/project', [ { 'customer' : 'CUSTOMER', 'type' : 'TYPE', 'name' : 'PROJECTNAME', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : 'start', 'end' : 'end', 'tasks' : [ 'task1', 'task2' ], 'grand_total' : 4, 'expences' : 4, 'responsible' : { '_id' : '1'*24, 'name' : 'Another Admin'}, 'employees' : [ { '_id' : '1'*24, 'name' : 'The employed administrator'} ] } ], { 'error' : None, 'ids' : [ '' ] })
    # Get the inserted project by NAME
    _assert('/get/project', [ { 'name' : 'PROJECTNAME' }, { 'contact_person' : 1, '_id' : 0 } ], { 'error': None, 'records' : [ { 'contact_person' : 'contact_person'  } ] })
    # Get the inserted project by responsible
    _assert('/get/project', [ { 'responsible._id' : '1'*24  }, { 'contact_person' : 1, '_id' : 0 } ], { 'error': None, 'records' : [ { 'contact_person' : 'contact_person'  } ] })
    # Get the inserted project by employers
    _assert('/get/project', [ { 'employees._id' : '1'*24 } , { 'contact_person' : 1, '_id' : 0 } ], { 'error': None, 'records' : [ { 'contact_person' : 'contact_person'  } ] })
    # Delete the one inserted by employers
    _assert('/remove/project', [ { 'employees._id' : '1'*24 } ], { 'error' : None })
    # Get the empty customers list
    _assert('/get/project', [ { 'employees._id' : '1'*24 }, { '_id' : 1 } ], { 'error': None, 'records' : [ ] })
        
    ## NEW USER LOGIN
    # Add one user with password, should login
    _assert('/add/user', [ { 'name' : 'NAME_USER_LOGIN_TEST', 'surname' : 'SURNAME', 'username' : 'NEW_USER_WITH_PWD', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ], { 'error' : None, 'ids' : [ '' ] })
    # Add user without password, should raise error
    _assert('/add/user', [ { 'name' : 'NAME_USER_LOGIN_TEST', 'surname' : 'SURNAME', 'username' : 'NEW_USER_WITH_NO_PWD', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : '', 'salt' : 'RANDOM_UNUSED_SALT', 'salary' : []  } ], { 'error' : 'ValidationError: Expected nonempty password', 'ids' : [ ] })
    # Check if can't login with NEW_USER_WITH_NO_PWD
    _login({'username' : 'NEW_USER_WITH_NO_PWD', 'password' : '' })
    _assert_page_contains('Timesheet login', True)
    # Check if can login with NEW_USER_WITH_PWD
    _login({'username' : 'NEW_USER_WITH_PWD', 'password' : 'mypassword' })
    _assert_page_contains('Timesheet login', False)
    # Relogin as admin
    _login(admin_credentials)
    # Delete both user in one request
    _assert('/remove/user', [ { 'name' : 'NAME_USER_LOGIN_TEST' } ], { 'error' : None })
    # Check presence
    _assert('/get/user', [ { 'name' : 'NAME_USER_LOGIN_TEST' }, { '_id' : 1 } ], { 'error': None, 'records' : [ ] })
    
    # TEST UPDATE
    
    # Add one customer (return one id)
    json_returned = _assert('/add/customer', [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTOMAIL', 'description' : 'CUSTODESC' } ], { 'error' : None, 'ids' : [ '' ] })
    # Get the inserted customer by id
    _assert('/get/customer', [ { '_id' : json_returned['ids'][0] }, { '_id' : 1 } ], { 'error': None, 'records' : [ { '_id' : ''   } ] })
    # Update name
    _assert('/update/customer', { '_id' : json_returned['ids'][0], 'name' : 'CUSTOMERNEWNAME', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTOMAIL', 'description' : 'CUSTODESC' }, { 'error': None })
    # Check if the inserted customer by id is modified
    _assert('/get/customer', [ { '_id' : json_returned['ids'][0] }, { '_id' : 1 } ], { 'error': None, 'records' : [ { '_id' : '' } ] })
    # Delete both user in one request
    _assert('/remove/customer', [ { '_id' : json_returned['ids'][0]} ], { 'error' : None })
    
    # TEST SCHEMA OPTIONS CONSTRAINTS
    _assert('/add/user', [ { 'name' : 'NAME_USER_LOGIN_TEST', 'surname' : 'SURNAME', 'username' : 'NEW_USER_WITH_PWD', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'WRONG_GROUP', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ], { 'error' : "ValidationError: Value u'WRONG_GROUP' for field 'group' is not in the enumeration: %s" % (str(users_groups)), 'ids' : [ ] })


    # TEST PERMISSIONS LIMITATIONS
    # GET admin password
    _assert('/get/user', [ { 'username' : 'ts_admin' }, { 'password' : 1} ], { 'error' : "ValidationError: Field 'password' is restricted for current user", 'records' : [ ] })
    # Add user in group employee for following tests
    _assert('/add/user', [ { 'name' : 'NAME', 'surname' : 'SURNAME', 'username' : 'PERM_TEST', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ], { 'error' : None, 'ids' : [ '' ] })
    # Add project for following tests
    _assert('/add/project', [ { 'customer' : 'CUSTOMER', 'type' : 'TYPE', 'name' : 'NAME', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : 'start', 'end' : 'end', 'tasks' : [ 'task1', 'task2' ], 'grand_total' : 4, 'expences' : 4, 'responsible' : { '_id' : '1'*24, 'name' : 'The administrator'}, 'employees' : [ { '_id' : '1'*24, 'name' : 'The employed administrator'} ] } ], { 'error' : None, 'ids' : [ '' ] })
    
    # Check if can login with NEW_USER_WITH_PWD
    _login({'username' : 'PERM_TEST', 'password' : 'mypassword' })
    _assert_page_contains('Timesheet login', False)

    # GET his own password
    _assert('/get/user', [ { 'username' : 'PERM_TEST' }, { 'password' : 1} ], { 'error' : "ValidationError: Field 'password' is restricted for current user", 'records' : [ ] })
    # GET other employee surname
    _assert('/get/user', [ { 'username' : admin_credentials['username'] }, { 'surname' : 1 } ], { 'error' : "ValidationError: Field 'username' is restricted for current user", 'records' : [ ] })
    # REMOVE himself
    _assert('/remove/user', [ { 'username' : 'PERM_TEST' } ], { 'error' : "ValidationError: Action 'remove' in 'user' is restricted for current user" })
    # Add new employee 
    _assert('/add/user', [ { 'name' : 'NAME', 'surname' : 'SURNAME', 'username' : 'PERM_TEST2', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [] } ], { 'error' : "ValidationError: Action 'add' in 'user' is restricted for current user", 'ids' : [ ] })
    # Get projects of other users
    _assert('/get/project', [ { 'name' : 'NAME' }, { 'customer' : 1 } ], { 'error' : None, 'records' : [ ] })
    # Get explicitely admin projects 
    _assert('/get/project', [ { 'responsible' : { '_id' : '1'*24 } }, { 'customer' : 1 } ], { 'error' : "ValidationError: Field 'responsible' is restricted for current user", 'records' : [ ] })
    # Wrongly delete added project
    _assert('/remove/project', [ { 'employees._id' : '1'*24 } ], { 'error' : "ValidationError: Action 'remove' in 'project' is restricted for current user" })
   

    # Check if normal user can see user management in admin menu
    _assert_page_contains('/index/users', False)
    # Relogin as admin
    _login(admin_credentials)
    _assert_page_contains('/index/users', True)    
    # Delete previously added test user
    _assert('/remove/user', [ { 'username' : 'PERM_TEST' } ], { 'error' : None })
    # Delete previously added project
    _assert('/remove/project', [ { 'employees._id' : '1'*24 } ], { 'error' : None })
    
    
    ## API DAYS
    # Insert a day with no user
    _assert('/data/push_days', [ {'date': '2000-01-01' }
                                ], { 'error' : None })   
    # Insert wrongly a day with multiple users
    _assert('/data/push_days', [ {'date': '2000-01-01', 
                                  'users': [ 
                                            { 'user_id' : '111111111111111111111111', 
                                             'hours': []
                                             },
                                             { 'user_id' : '0', 
                                             'hours': []
                                             } 
                                            ]
                                  }
                                ], { 'error' : 'ValidationError: Push only one user per day' })
    # Insert the day 17 for user  '111111111111111111111111'                                      
    _assert('/data/push_days', [ {'date': '2000-10-17', 
                                  'users': [ 
                                            { 'user_id' : '111111111111111111111111', 
                                             'hours': [
                                                       {u'note': u'FIRST 4 HOURS', u'task': u'', u'isextra': False, u'project': u'524efeef2c066a1bc6000001', u'amount': u'4'}, 
                                                       {u'note': u'SECOND 4 HOURS', u'task': u'', u'isextra': False, u'project': u'524efeef2c066a1bc6000001', u'amount': u'4'}
                                                       ]
                                             }
                                            ]
                                  }
                                ], { 'error' : None })   
    # Push in the day 17 also user  '0'                                      
    _assert('/data/push_days', [ {'date': '2000-10-17', 
                                  'users': [ 
                                            { 'user_id' : '0', 
                                             'hours': []
                                             }
                                            ]
                                  }
                                ], { 'error' : None })                                            
    # Push also the year after the user  '0'                                      
    _assert('/data/push_days', [ {'date': '2001-02-02', 
                                  'users': [ 
                                            { 'user_id' : '0', 
                                             'hours': []
                                             }
                                            ]
                                  }
                                ], { 'error' : None })   
    # Get the day 2000-10-17 for user 0                                        
    _assert('/data/search_days', { 'date_from' : '2000-10-17', 'date_to' : '2000-10-17', 'user_id' : '0' }, {u'records': [{u'date': u'2000-10-17', u'_id': '', u'users': [{u'hours': [], u'user_id': u'0'}]}], u'error': None})
    # Get the years 2000-01-01 2003-01-01 for user 0
    _assert('/data/search_days', { 'date_from' : '2000-01-01', 'date_to' : '2003-01-01', 'user_id' : '0' }, {u'records': [{u'date': u'2000-10-17', u'_id': '', u'users': [{u'hours': [], u'user_id': u'0'}]}, {u'date': u'2001-02-02', u'_id': '', u'users': [{u'hours': [], u'user_id': u'0'}]}], u'error': None} )
    # Get unexistant user 2
    _assert('/data/search_days', { 'date_from' : '2000-01-01', 'date_to' : '2003-01-01', 'user_id' : '2' }, {u'records': [ ], u'error': None} )
    # Get empty span 
    _assert('/data/search_days', { 'date_from' : '2010-01-01', 'date_to' : '2011-01-01', 'user_id' : '0' }, {u'records': [ ], u'error': None} )
    # Delete all inserted days
    _assert('/remove/day', [ { "date" :  "2000-10-17" },  { "date" :  "2000-01-01" },  { "date" :  "2001-02-02" } ] , { 'error' : None })
    
    
if __name__ == "__main__":
    
    if len(sys.argv) >= 3:
        # Credentials
        admin_credentials = {'username': sys.argv[1], 'password': sys.argv[2]}
        main(admin_credentials)
    else:
        print 'Error, run with:\n%s <username> <password>' % (sys.argv[0])



