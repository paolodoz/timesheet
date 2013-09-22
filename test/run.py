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
    
    # Dirty code to remove records real '_id's to simplify the comparison
    if 'records' in json_returned:
        records = json_returned['records']
    else:
        records = [ json_returned ]
    
    for rec in records:
        if '_id' in rec:
            del rec['_id']

    #print 'RETURNED ', json_returned, '\nEXPECTED ', json_expected
    assert(json_returned == json_expected)


# LOGIN
_login(credentials)

## TEST BAD REQUESTS
# Add unexistant collection
_assert('/add/wrong', { 'wrong': 'param' }, {'error' : "KeyError: 'wrong'" })
# Add user with unsupported param 
_assert('/add/user', { 'wrong': 'param' }, {'error' : 'ValidationError: Required field \'city\' is missing' })

## API CUSTOMER
_assert('/remove/customer', { 'name' : 'CUSTOMERTEST',  }, { 'error' : None })
_assert('/add/customer', { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT' }, { 'error' : None })
_assert('/get/customer', { 'name' : 'CUSTOMERTEST' }, { 'error': None, 'records' : [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT' } ] })

## API USER
_assert('/remove/user', { 'name' : 'USERTEST',  }, { 'error' : None })
_assert('/add/user', { 'name' : 'USERTEST', 'surname' : 'SURNAME', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY' }, { 'error' : None })
_assert('/get/user', { 'name' : 'USERTEST' }, { 'error': None, 'records' : [ { 'name' : 'USERTEST', 'surname' : 'SURNAME', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY' } ] })

