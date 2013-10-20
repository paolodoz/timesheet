from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager


class UserAPIAsAdmin(TestClassBase):
    
    def test_user_ok(self):
        # Remove already unexistant user
        self._assert_req('/remove/user', [ { 'name' : 'UNEXISTANT'  } ], { 'error' : None  })
         
        # Add two elements USERTEST1 and USERTEST2
        self._assert_req('/add/user', [ { 'name' : 'USERTEST1', 'surname' : 'SURNAME', 'username' : 'USERNAME1' , 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : []  }, { 'name' : 'USERTEST2', 'surname' : 'SURNAME', 'username' : 'USERNAME2' , 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : []  } ], { 'error' : None, 'ids' : [ '', '' ] })
        # Delete USERTEST1
        self._assert_req('/remove/user', [ { 'name' : 'USERTEST1'  }, { 'name' : 'USERTEST2'  } ], { 'error' : None })
        # Check if USERTEST1 is deleted
        self._assert_req('/get/user', [ { 'name' : 'USERTEST1' }, { '_id' : 1 } ], { 'error': None, 'records' : [ ] })
 
        # Delete the remaining user
        self.execOnTearDown.append(('/remove/user', [ { 'name' : 'USERTEST2'  } ], { 'error' : None }))
 
    def test_username_uniqueness(self):
         
        # Add one customer (return one id)
        self._assert_req('/add/user', [ { 'name' : 'UNIQTEST', 'surname' : 'SURNAME', 'username' : 'USERNAME', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [] } ], { 'error' : None, 'ids' : [ '' ] })
        # Add a double customer (UNIQ test)
        self._assert_req('/add/user', [ { 'name' : 'UNIQTEST', 'surname' : 'SURNAME2', 'username' : 'USERNAME', 'email' : 'EMAIL2', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ], { 'error' : None, 'ids' : [ '' ] })
        # Get the inserted customer (is only one because UNIQ)
        self._assert_req('/get/user', [ { 'name' : 'UNIQTEST' }, { 'surname' : 1, '_id' : 0 } ], { 'error': None, 'records' : [ { 'surname' : 'SURNAME'  } ] })
         
        # Delete the inserted day
        self.execOnTearDown.append(('/remove/user', [ { 'name' : 'UNIQTEST'  } ], { 'error' : None }))
         
        
    def test_user_add(self):
        
        # Add one user with password, should login
        json_user_pwd = self._assert_req('/add/user', [ { 'name' : 'NEW_USER_WITH_PWD', 'surname' : 'SURNAME', 'username' : 'NEW_USER_WITH_PWD', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'MOB1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : []  } ], { 'error' : None, 'ids' : [ '' ] })
        id_user_pwd = json_user_pwd['ids'][0]
        
        # Add user without password, should raise error
        json_user_nopwd = self._assert_req('/add/user', [ { 'name' : 'NEW_USER_WITH_NO_PWD', 'surname' : 'SURNAME', 'username' : 'NEW_USER_WITH_NO_PWD', 'email' : 'EMAIL', 'phone' : '123456789', 'mobile' : 'MOB1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : '', 'salt' : 'RANDOM_UNUSED_SALT', 'salary' : []  } ], { 'error' : "ValidationError: Error '' is not valid", 'ids' : [ ] })
        
        # Check if can't login with NEW_USER_WITH_NO_PWD
        credentials = {'username' : 'NEW_USER_WITH_NO_PWD', 'password' : '' }
        self._login(credentials)
        self._assert_unlogged()
        
        # Check if can login with NEW_USER_WITH_PWD
        credentials = {'username' : 'NEW_USER_WITH_PWD', 'password' : 'mypassword' }
        self._login(credentials)
        self._assert_logged(credentials)
        
        # Delete the inserted user
        self.execOnTearDown.append(('/remove/user', [ { '_id' :  json_user_pwd } ], { 'error' : None }))
 