import urllib2, urllib, json, os, sys, types
from cookielib import CookieJar
from core.validation.validation import recursive_replace
import unittest, copy

admin_credentials = { 'username' : 'usr', 'password' : 'pwd' }
admin_data = [ { 'password' : admin_credentials['password'], 
              'name' : admin_credentials['username'], 
              'surname' : 'Default', 
              'username':  admin_credentials['username'], 
              'email' : 'admin@localhost', 
              'phone' : '', 
              'mobile' : '', 
              'city' : '', 
              'group' : 'administrator', 
              'salary' : []  } ]

url = "https://localhost:9090"

def _function_clean_id(container):
    if isinstance(container,types.DictType):
        if 'ids' in container:
            container['ids'] = ['']*len(container['ids'])
        else:
            for k, v in container.items():
                if (k == '_id' or k.endswith('._id')) and isinstance(container[k], types.StringTypes):
                    container[k] = ''

def clean_id(json_in):
    return recursive_replace(json_in.copy(), _function_clean_id)

class TestClassBase(unittest.TestCase):
    
    def setUp(self):

        self.maxDiff = None
        self.execOnTearDown = []
        
        self.cookies = CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        self._assert_unlogged()
        self._login(admin_credentials, 'administrator')
        self._assert_logged(admin_credentials)
        self.admin_data = admin_data
    
    def _login(self, credentials, group):
        self.cookies.clear()
        encoded_credentials = urllib.urlencode(credentials)
        self.opener.open(url + "/auth/login", encoded_credentials)
        self.group = group
    
    def _assert_logged(self, credentials):
        
        json_out = self._request('/me', {})
        json_out['notifications'] = 0
        self.assertEqual(clean_id(copy.deepcopy(json_out)), { 'username' : credentials['username'], '_id' : '', 'group' : self.group, 'notifications' : 0 })
        
    def _assert_unlogged(self):
        self.assertEqual(urllib2.urlopen(url + '/me').geturl(), url + '/auth/login')
        
    def _request(self, uri, json_in):
        request = urllib2.Request('https://localhost:9090/%s' % uri.lstrip('/'), data=json.dumps(json_in), headers={'Content-Type': 'application/json'})
        return json.loads(self.opener.open(request).read())
        
    def _assert_req(self, uri, json_in, json_expected):
        json_out = self._request(uri, json_in)
#         import pprint
#         print 'RETURNED:', pprint.pprint(clean_id(copy.deepcopy(json_out)))
#         print 'EXPECTED:', pprint.pprint(json_expected)
#         print 'EQ:', clean_id(copy.deepcopy(json_out)) == json_expected
        self.assertEqual(clean_id(copy.deepcopy(json_out)), json_expected)
        return json_out
        
    def tearDown(self):
        
        self._login(admin_credentials, 'administrator')
        self._assert_logged(admin_credentials)
        
        for command in self.execOnTearDown:
            uri, json_in, json_expected = command
            
            self.assertEqual(clean_id(self._request(uri, json_in)), json_expected)

    def _plain_request(self, uri = ''):
        return self.opener.open('https://localhost:9090/' + uri).read()        
        
class TestCaseAsEmployee(TestClassBase):
    
    def setUp(self):
        TestClassBase.setUp(self)
        self._add_user_data()
        self._log_as_user()


    def _add_user_data(self):
                
        uri = '/add/user'
        self.employee_data = [ { 'name' : 'USERTEST', 'surname' : 'SURNAME', 'username' : 'EMPNAME', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [] } ]
        
        employee_json = self._assert_req(uri, self.employee_data, { 'error' : None, 'ids' : [ '' ] })
        self.employee_id = employee_json['ids'][0]
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.employee_id } ], { 'error' : None }))
        
    def _log_as_user(self):     
        employee_credentials = { 'username' : 'EMPNAME', 'password' : 'mypassword' }
        self._login(employee_credentials, 'employee')
        self._assert_logged(employee_credentials)
    
class TestCaseAsManager(TestClassBase):

    def setUp(self):
        TestClassBase.setUp(self)
        self._add_user_data()
        self._log_as_user()
        
    def _add_user_data(self):        
        # Add manager user
        uri = '/add/user'
        self.manager_data = [ { 'name' : 'MANAGER', 'surname' : 'MANAGERSURNAME', 'username' : 'MANAGER', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'project manager', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ]
    
        manager_json = self._assert_req(uri, self.manager_data, { 'error' : None, 'ids' : [ '' ] })
        self.manager_id = manager_json['ids'][0]
        
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.manager_id } ], { 'error' : None }))
      
    def _log_as_user(self):
        
        manager_credentials = { 'username' : 'MANAGER', 'password' : 'mypassword' }
        self._login(manager_credentials, 'project manager')
        self._assert_logged(manager_credentials)
                
                
                
class TestCaseAsAccount(TestClassBase):

    def setUp(self):
        TestClassBase.setUp(self)
        self._add_user_data()
        self._log_as_user()
        
    def _add_user_data(self):        
        # Add manager user
        uri = '/add/user'
        self.account_data = [ { 'name' : 'ACCOUNT', 'surname' : 'ACCOUNTSURNAME', 'username' : 'ACCOUNT', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'account', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ]
    
        account_json = self._assert_req(uri, self.account_data, { 'error' : None, 'ids' : [ '' ] })
        self.account_id = account_json['ids'][0]
        
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.account_id } ], { 'error' : None }))
      
    def _log_as_user(self):
        
        account_credentials = { 'username' : 'ACCOUNT', 'password' : 'mypassword' }
        self._login(account_credentials, 'account')
        self._assert_logged(account_credentials)