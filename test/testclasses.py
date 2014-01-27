import urllib2, urllib, json, os, sys, types
from cookielib import CookieJar
from core.validation.validation import recursive_replace
import unittest, copy

# TODO: get credentials from config.yaml
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
              'salary' : [],
              'status' : 'active'  } ]

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
        self._login(admin_data[0], 'administrator')
        self._assert_logged(admin_data[0])
        self.admin_data = admin_data
    
    def _login(self, data, group):
        self.cookies.clear()
        encoded_credentials = urllib.urlencode({ 'username' : data['username'], 'password' : data['password']})
        self.opener.open(url + "/auth/login", encoded_credentials)
        self.group = group
    
    def _assert_logged(self, data, notifications = None):
        
        json_out = self._request('/me', {})
        
        if notifications != None:
            self.assertEqual({ 'username' : json_out['username'], 'group' : json_out['group'], 'notifications' : json_out['notifications'] }, { 'username' : data['username'], 'group' : self.group, 'notifications' : notifications })
        else:
           self.assertEqual({ 'username' : json_out['username'], 'group' : json_out['group'] }, { 'username' : data['username'], 'group' : self.group })
 
        
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
        
        self._login(self.admin_data[0], 'administrator')
        self._assert_logged(self.admin_data[0])
        
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
        self.employee_data = [ { 'name' : 'USERTEST', 'surname' : 'SURNAME', 'username' : 'EMPNAME', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'status' : 'active' } ]
        
        employee_json = self._assert_req(uri, self.employee_data, { 'error' : None, 'ids' : [ '' ] })
        self.employee_id = employee_json['ids'][0]
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.employee_id } ], { 'error' : None }))
        
    def _log_as_user(self):     
        self._login(self.employee_data[0], 'employee')
        self._assert_logged(self.employee_data[0])
    
class TestCaseAsManager(TestClassBase):

    def setUp(self):
        TestClassBase.setUp(self)
        self._add_user_data()
        self._log_as_user()
        
    def _add_user_data(self):        
        # Add manager user
        uri = '/add/user'
        self.manager_data = [ { 'name' : 'MANAGER', 'surname' : 'MANAGERSURNAME', 'username' : 'MANAGER', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'project manager', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'status' : 'active'  } ]
    
        manager_json = self._assert_req(uri, self.manager_data, { 'error' : None, 'ids' : [ '' ] })
        self.manager_id = manager_json['ids'][0]
        
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.manager_id } ], { 'error' : None }))
      
    def _log_as_user(self):
        self._login(self.manager_data[0], 'project manager')
        self._assert_logged(self.manager_data[0])
                
                
                
class TestCaseAsAccount(TestClassBase):

    def setUp(self):
        TestClassBase.setUp(self)
        self._add_user_data()
        self._log_as_user()
        
    def _add_user_data(self):        
        # Add manager user
        uri = '/add/user'
        self.account_data = [ { 'name' : 'ACCOUNT', 'surname' : 'ACCOUNTSURNAME', 'username' : 'ACCOUNT', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'account', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'status' : 'active'  } ]
    
        account_json = self._assert_req(uri, self.account_data, { 'error' : None, 'ids' : [ '' ] })
        self.account_id = account_json['ids'][0]
        
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.account_id } ], { 'error' : None }))
      
    def _log_as_user(self):
        
        account_credentials = { 'username' : 'ACCOUNT', 'password' : 'mypassword' }
        self._login(self.account_data[0], 'account')
        self._assert_logged(self.account_data[0])
        
        
class TestCaseMultipleUsers(TestClassBase):
    def setUp(self):
        TestClassBase.setUp(self)
        self._add_multi_user_data()    

    def _add_multi_user_data(self):        
        uri = '/add/user'
        
        self.account_data = [ { 'name' : 'ACCOUNT', 'surname' : 'ACCOUNTSURNAME', 'username' : 'ACCOUNT', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'account', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'status' : 'active'  } ]
        account_json = self._assert_req(uri, self.account_data, { 'error' : None, 'ids' : [ '' ] })
        self.account_id = account_json['ids'][0]
        
        self.employee_data = [ { 'name' : 'USERTEST', 'surname' : 'SURNAME', 'username' : 'EMPNAME', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'status' : 'active' } ]
        employee_json = self._assert_req(uri, self.employee_data, { 'error' : None, 'ids' : [ '' ] })
        self.employee_id = employee_json['ids'][0]
        
        self.manager_data = [ { 'name' : 'MANAGER', 'surname' : 'MANAGERSURNAME', 'username' : 'MANAGER', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'project manager', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'status' : 'active'  } ]
        manager_json = self._assert_req(uri, self.manager_data, { 'error' : None, 'ids' : [ '' ] })
        self.manager_id = manager_json['ids'][0]
        
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.account_id }, { '_id' : self.manager_id }, { '_id' : self.employee_id } ], { 'error' : None }))        

    def _log_as_account(self):
        self._login(self.account_data[0], 'account')
        self._assert_logged(self.account_data[0])  

    def _log_as_manager(self):
        self._login(self.manager_data[0], 'project manager')
        self._assert_logged(self.manager_data[0])
        
    def _log_as_employee(self):
        self._login(self.employee_data[0], 'employee')
        self._assert_logged(self.employee_data[0])       
        
    def _log_as_admin(self):     
        self._login(self.admin_data[0], 'administrator')
        self._assert_logged(self.admin_data[0])
        