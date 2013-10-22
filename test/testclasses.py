import urllib2, urllib, json, os, sys, types
from cookielib import CookieJar
from core.validation import recursive_replace
import unittest, copy

admin_credentials = { 'username' : 'usr', 'password' : 'pwd' }
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
        
        self.execOnTearDown = []
        
        self.cookies = CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        self._assert_unlogged()
        self._login(admin_credentials)
        self._assert_logged(admin_credentials)
    
    def _login(self, credentials):
        self.cookies.clear()
        encoded_credentials = urllib.urlencode(credentials)
        self.opener.open(url + "/auth/login", encoded_credentials)
    
    def _assert_logged(self, credentials):
        self._assert_req('/me', None, { 'username' : credentials['username'], '_id' : '' })
        
    def _assert_unlogged(self):
        self.assertEqual(urllib2.urlopen(url + '/me').geturl(), url + '/auth/login')
        
    def _request(self, uri, json_in):
        request = urllib2.Request('https://localhost:9090/%s' % uri.lstrip('/'), data=json.dumps(json_in), headers={'Content-Type': 'application/json'})
        return json.loads(self.opener.open(request).read())
        
    def _assert_req(self, uri, json_in, json_expected):
        json_out = self._request(uri, json_in)
        print json_out
        self.assertEqual(clean_id(copy.deepcopy(json_out)), json_expected)
        return json_out
        
    def tearDown(self):
        
        self._login(admin_credentials)
        self._assert_logged(admin_credentials)
        
        for command in self.execOnTearDown:
            uri, json_in, json_expected = command
            
            self.assertEqual(clean_id(self._request(uri, json_in)), json_expected)

    def _plain_request(self, uri = ''):
        return self.opener.open('https://localhost:9090/' + uri).read()        
        
class TestCaseAsEmployee(TestClassBase):
    def setUp(self):
        TestClassBase.setUp(self)
        
        uri = '/add/user'
        json_in = [ { 'name' : 'USERTEST', 'surname' : 'SURNAME', 'username' : 'USERNAME', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [] } ]
        
        employee_json = self._assert_req(uri, json_in, { 'error' : None, 'ids' : [ '' ] })
        self.employee_id = employee_json['ids'][0]
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.employee_id } ], { 'error' : None }))
        
        
        employee_credentials = { 'username' : 'USERNAME', 'password' : 'mypassword' }
        self._login(employee_credentials)
        self._assert_logged(employee_credentials)

    
class TestCaseAsManager(TestClassBase):
    def setUp(self):
        TestClassBase.setUp(self)
        
        # Add manager user
        uri = '/add/user'
        json_in = [ { 'name' : 'MANAGER', 'surname' : 'MANAGERSURNAME', 'username' : 'MANAGER', 'email' : 'EMAIL@DOMAIN', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'project manager', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ]
    
        manager_json = self._assert_req(uri, json_in, { 'error' : None, 'ids' : [ '' ] })
        self.manager_id = manager_json['ids'][0]
        
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.manager_id } ], { 'error' : None }))
        
        # Add managed projects
        uri = '/add/project'
        json_in = [
                    { 'name' : 'MANAGEDPROJECT1', 'customer' : 'CUSTOMER1', 'type' : 'TYPE1', 'description' : 'description1', 'contact_person' : 'contact_person1', 'start' : '2000-01-02', 'end' : '2000-01-03', 'tasks' : [ 'task1', 'task2' ], 'grand_total' : 4, 'expences' : 4, 'responsible' : { '_id' : self.manager_id, 'name' : 'The manager'}, 'employees' : [ { '_id' : '1'*24, 'name' : 'The employed administrator'} ] }, 
                    { 'name' : 'MANAGEDPROJECT2', 'customer' : 'CUSTOMER2', 'type' : 'TYPE2', 'description' : 'description2', 'contact_person' : 'contact_person2', 'start' : '2000-01-01', 'end' : '2000-01-05', 'tasks' : [ 'task1', 'task2' ], 'grand_total' : 4, 'expences' : 4, 'responsible' : { '_id' : self.manager_id, 'name' : 'The manager'}, 'employees' : [ { '_id' : '7'*24, 'name' : 'Another employee'} ] } 
                    ]
        
        
        projects_json = self._assert_req(uri, json_in, { 'error' : None, 'ids' : [ '', '' ] })
        self.managed_projects = projects_json['ids']

        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.managed_projects[0] }, { '_id' : self.managed_projects[1] } ], { 'error' : None }))
        
        employee_credentials = { 'username' : 'MANAGER', 'password' : 'mypassword' }
        self._login(employee_credentials)
        self._assert_logged(employee_credentials)
                