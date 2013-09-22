import urllib2, urllib, json, os
from cookielib import CookieJar


# Credentials
credentials = {'username': 'test', 'password': 'test'}

cj = CookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def _login(values):
    data = urllib.urlencode(values)
    opener.open("https://localhost:9090/auth/login", data)

def _assert(uri, json_in, json_out):
    request = urllib2.Request('https://localhost:9090/%s' % uri.lstrip('/'), data=json.dumps(json_in), headers={'Content-Type': 'application/json'})
    json_returned = json.loads(opener.open(request).read())
    assert(json_returned == json_out)

    
_login(credentials)
_assert('/add/wrong', { 'wrong': 'param' }, {'error' : "KeyError: 'wrong'"})
_assert('/add/user', { 'wrong': 'param' }, {'error' : 'ValidationError: Required field \'city\' is missing'})