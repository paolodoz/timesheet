#!/usr/bin/env python
import urllib2, urllib, json, os
from cookielib import CookieJar


# Credentials
credentials = {'username': 'test', 'password': 'test'}

cj = CookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# Login procedure using credentials
def _login(values):
    data = urllib.urlencode(values)
    opener.open("https://localhost:9090/auth/login", data)

# Assert procedure
def _assert(uri, json_in, json_expected):
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
    
    print '\nPOST ', uri , json_in, '\nRETURNED ', json_returned_noid, '\nEXPECTED ', json_expected
    assert(json_returned_noid == json_expected)
    print 'OK!'
    
    return json_returned


# LOGIN
_login(credentials)

## TEST BAD REQUESTS
# Add directly json without list
_assert('/add/wrong', { 'single': 'dict' }, {'error' : "ValidationError: list expected, not 'dict'", 'ids' : [] })
# Add unexistant collection
_assert('/add/wrong', [ { 'wrong': 'param' } ], {'error' : "KeyError: 'wrong'", 'ids' : [] })
# Add user with unsupported param 
_assert('/add/user', [ { 'wrong': 'param' } ], {'error' : 'ValidationError: Required field \'username\' is missing', 'ids' : []  })

## API CUSTOMER
# Remove already unexistant customer
_assert('/remove/customer', [ { 'name' : 'CUSTOMERTEST' } ], { 'error' : None  })
# Add one customer (return one id)
json_returned = _assert('/add/customer', [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTOMAIL', 'description' : 'CUSTODESC' } ], { 'error' : None, 'ids' : [ '' ] })
# Get the inserted customer by name
_assert('/get/customer', { 'name' : 'CUSTOMERTEST' }, { 'error': None, 'records' : [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', '_id' : '', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTOMAIL', 'description' : 'CUSTODESC'   } ] })
# Get the inserted customer by id
_assert('/get/customer', { '_id' : json_returned['ids'][0] }, { 'error': None, 'records' : [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', '_id' : '', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTOMAIL', 'description' : 'CUSTODESC'   } ] })
# Remove customer by id
_assert('/remove/customer', [ { '_id' : json_returned['ids'][0] } ], { 'error' : None  })
# Check if collection is empty
_assert('/get/customer', { }, { 'error': None, 'records' : [ ] })

## API USER
# Remove already unexistant user
_assert('/remove/user', [ { 'name' : 'USERTEST'  } ], { 'error' : None  })
# Add one customer (return one user)
_assert('/add/user', [ { 'name' : 'USERTEST', 'surname' : 'SURNAME', 'username' : 'USERNAME', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'role' : 'user' } ], { 'error' : None, 'ids' : [ '' ] })
# Get the inserted customer
_assert('/get/user', { 'name' : 'USERTEST' }, { 'error': None, 'records' : [ { 'name' : 'USERTEST', 'surname' : 'SURNAME', 'username' : 'USERNAME' , 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', '_id' : '' , 'role' : 'user' } ] })
# Delete the one inserted
_assert('/remove/user', [ { 'name' : 'USERTEST'  } ], { 'error' : None })
# Get the empty customers list
_assert('/get/user', { 'name' : 'USERTEST' }, { 'error': None, 'records' : [ ] })
# Add two elements USERTEST1 and USERTEST2
_assert('/add/user', [ { 'name' : 'USERTEST1', 'surname' : 'SURNAME', 'username' : 'USERNAME1' , 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'role' : 'user' }, { 'name' : 'USERTEST2', 'surname' : 'SURNAME', 'username' : 'USERNAME2' , 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'role' : 'user' } ], { 'error' : None, 'ids' : [ '', '' ] })
# Delete USERTEST1
_assert('/remove/user', [ { 'name' : 'USERTEST1'  } ], { 'error' : None })
# Check if USERTEST1 is deleted
_assert('/get/user', { 'name' : 'USERTEST1' }, { 'error': None, 'records' : [ ] })
# Delete all users
_assert('/remove/user', [ {  } ], { 'error' : None })
# Check if collection is empty
_assert('/get/user', { }, { 'error': None, 'records' : [ ] })


