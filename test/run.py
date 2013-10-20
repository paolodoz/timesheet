#!/usr/bin/env python
import urllib2, urllib, json, os, sys
from cookielib import CookieJar


# Possible users groups
users_groups = [ 'administrator', 'employee', 'project manager']


cj = CookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def _login(values):
    """Login procedure using admin_credentials"""
    print '\nLogin as \'%s\'' % (values['username'])
    cj.clear()
    data = urllib.urlencode(values)
    opener.open("https://localhost:9090/auth/login", data)
    

def _assert_page_contains(needle, check_contains=True):
    """Search needle in main page"""
    print 'CHECK if user GET %s return \'%s\'' % ('' if check_contains else 'does not', needle)
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
    elif 'ids' in json_returned_noid and json_returned_noid['ids']:
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


    # TEST PERMISSIONS LIMITATIONS
    # GET admin password
    _assert('/get/user', [ { '_id' : '1'*24 }, { 'password' : 1} ], { 'error' : "TSValidationError: Field 'password' is restricted for current user", 'records' : [ ] })
    # Add user in group employee for following tests
    employee_json = _assert('/add/user', [ { 'name' : 'NAME', 'surname' : 'SURNAME', 'username' : 'PERM_TEST', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ], { 'error' : None, 'ids' : [ '' ] })
    # Add project manager for following tests
    manager_json = _assert('/add/user', [ { 'name' : 'MANAGER', 'surname' : 'MANAGERSURNAME', 'username' : 'MANAGER', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'project manager', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ], { 'error' : None, 'ids' : [ '' ] })
    # Add project managed by MANAGER for following tests
    _assert('/add/project', [ { 'name' : 'MANAGEDPROJECT', 'customer' : 'CUSTOMER', 'type' : 'TYPE', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : 'start', 'end' : 'end', 'tasks' : [ 'task1', 'task2' ], 'grand_total' : 4, 'expences' : 4, 'responsible' : { '_id' : manager_json['ids'][0], 'name' : 'The manager'}, 'employees' : [ { '_id' : employee_json['ids'][0], 'name' : 'The employed administrator'} ] } ], { 'error' : None, 'ids' : [ '' ] })
    # Add project managed by admin
    _assert('/add/project', [ { 'name' : 'ADMINPROJECT', 'customer' : 'CUSTOMER', 'type' : 'TYPE', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : 'start', 'end' : 'end', 'tasks' : [ 'task1', 'task2' ], 'grand_total' : 4, 'expences' : 4, 'responsible' : { '_id' : '1'*24, 'name' : 'The admin'}, 'employees' : [ { '_id' : employee_json['ids'][0], 'name' : 'The employed administrator'} ] } ], { 'error' : None, 'ids' : [ '' ] })
    
    # Add days for following tests
    _assert('/data/push_days', [ {'date': '2000-01-01', 'users': [ { 'user_id' : '111111111111111111111111', 'hours': [] } ] } ], { 'error' : None })    
    
    # Check if can login with NEW_USER_WITH_PWD
    _login({'username' : 'PERM_TEST', 'password' : 'mypassword' })
    _assert_page_contains('Timesheet login', False)

    # Get projects of other users
    _assert('/get/project', [ { 'name' : 'NAME' }, { 'customer' : 1 } ], { 'error' : "ValidationError: Error '{u'name': u'NAME'}' is not valid", 'records' : [ ] })
    # Get explicitely admin projects 
    _assert('/get/project', [ { 'responsible' : { '_id' : '1'*24 } }, { 'customer' : 1 } ], { 'error' : "ValidationError: Error '{u'responsible': {u'_id': u'111111111111111111111111'}}' is not valid", 'records' : [ ] })
    # Wrongly delete added project
    _assert('/remove/project', [ { 'employees._id' : '1'*24 } ], { 'error' : "TSValidationError: Action 'remove' in 'project' is restricted for current user" })
    # Wrongly get day from another users, returns error
    _assert('/data/search_days', { 'date_from' : '2000-01-01', 'date_to' : '2000-01-01', 'user_id' : '111111111111111111111111' }, { 'error': "ValidationError: Error '111111111111111111111111' is not valid"})
    
    # Relogin as manager
    _login({'username' : 'MANAGER', 'password' : 'mypassword' })
    _assert_page_contains('Timesheet login', False)   
    # Get all the projects of MANAGER
    _assert('/get/project', [ {  }, { 'customer' : 1 } ], {u'records': [], u'error': u"ValidationError: Error '{}' is not valid"})
    # Get project that MANAGER does not manage
    _assert('/get/project', [ { 'responsible._id' : manager_json['ids'][0], 'name' : 'ADMINPROJECT' }, { 'customer' : 1 } ], {u'records': [], u'error': None })
    # Get project that MANAGER manage
    _assert('/get/project', [ { 'responsible._id' : manager_json['ids'][0] }, { 'customer' : 1 } ], { u'records': [{u'customer': u'CUSTOMER', u'_id': ''}], u'error': None})


    # Relogin as admin
    _login(admin_credentials)
    # Delete previously added test user
    _assert('/remove/user', [ { 'username' : 'PERM_TEST' } ], { 'error' : None })
    # Delete previously added project
    _assert('/remove/project', [ { 'employees._id' : '1'*24 } ], { 'error' : None })
    
    
    ## API DAYS
    
    
if __name__ == "__main__":
    
    if len(sys.argv) >= 3:
        # Credentials
        admin_credentials = {'username': sys.argv[1], 'password': sys.argv[2]}
        main(admin_credentials)
    else:
        print 'Error, run with:\n%s <username> <password>' % (sys.argv[0])



