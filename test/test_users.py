from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager


class UserAPIAsAdmin(TestClassBase):
     
    def test_user_ok(self):
        # Remove already unexistant user
        self._assert_req('/remove/user', [ { 'name' : 'UNEXISTANT'  } ], { 'error' : None  })
          
        # Add two elements USERTEST1 and USERTEST2
        self._assert_req('/add/user', [ { 'name' : 'USERTEST1', 'surname' : 'SURNAME', 'username' : 'USERNAME1' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'contract' : 'oe', 'status' : 'active'  }, { 'name' : 'USERTEST2', 'surname' : 'SURNAME', 'username' : 'USERNAME2' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : [], 'contract' : 'oe', 'status' : 'active'   } ], { 'error' : None, 'ids' : [ '', '' ] })
        # Delete USERTEST1
        self._assert_req('/remove/user', [ { 'name' : 'USERTEST1'  }, { 'name' : 'USERTEST2'  } ], { 'error' : None })
        # Check if USERTEST1 is deleted
        self._assert_req('/get/user', [ { 'name' : 'USERTEST1' }, { '_id' : 1 }, { } ], { 'error': None, 'records' : [ ] })
  
        # Delete the remaining user
        self.execOnTearDown.append(('/remove/user', [ { 'name' : 'USERTEST2'  } ], { 'error' : None }))
        
        # Add one user with unknown group
        self._assert_req('/add/user', [ { 'name' : 'NEW_USER_NOGROUP', 'surname' : 'SURNAME', 'username' : 'NEW_USER_WITH_NO_PWD', 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'MOB1', 'city' : 'USERCITY', 'group' : 'EMPLOIERZ', 'password' : '', 'salt' : 'RANDOM_UNUSED_SALT', 'salary' : [], 'contract' : 'oe', 'status' : 'active'  } ], { 'error' : "ValidationError: u'EMPLOIERZ' is not one of ['administrator', 'employee', 'project manager', 'account']", 'ids' : [ ] })
        
        
    def test_user_private_values(self):
        
        user_data_pwd = [ { 'name' : 'NEW_USER_WITH_PWD', 'surname' : 'SURNAME', 'username' : 'NEW_USER_WITH_PWD', 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'MOB1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'contract' : 'oe', 'status' : 'active'  } ]
        json_user_pwd = self._assert_req('/add/user', user_data_pwd, { 'error' : None, 'ids' : [ '' ] })
        id_user_pwd = json_user_pwd['ids'][0]
        
        # Get contract and status "private" fields available to admin
        self._assert_req('/get/user', [ { 'name' : 'NEW_USER_WITH_PWD' }, { '_id' : 0, 'contract' : 1, 'status' : 1 }, { } ], { 'error': None, 'records' : [ { 'contract' : 'oe', 'status' : 'active' } ] })
         
        # Delete the inserted user
        self.execOnTearDown.append(('/remove/user', [ { '_id' :  id_user_pwd } ], { 'error' : None }))
  
    def test_username_uniqueness(self):
          
        # Add one customer (return one id)
        self._assert_req('/add/user', [ { 'name' : 'UNIQTEST', 'surname' : 'SURNAME', 'username' : 'USERNAME', 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'status' : 'active' } ], { 'error' : None, 'ids' : [ '' ] })
        # Add a double customer (UNIQ test)
        self._assert_req('/add/user', [ { 'name' : 'UNIQTEST', 'surname' : 'SURNAME2', 'username' : 'USERNAME', 'email' : 'EMAIL2@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'status' : 'active'  } ], { 'error' : "DuplicateKeyError internal exception", 'ids' : [ ] })
        # Get the inserted customer (is only one because UNIQ)
        self._assert_req('/get/user', [ { 'name' : 'UNIQTEST' }, { 'surname' : 1, '_id' : 0 }, { } ], { 'error': None, 'records' : [ { 'surname' : 'SURNAME'  } ] })
          
        # Delete the inserted day
        self.execOnTearDown.append(('/remove/user', [ { 'name' : 'UNIQTEST'  } ], { 'error' : None }))
          
         
    def test_user_add(self):
         
        # Add one user with password, should login
        user_data_pwd = [ { 'name' : 'NEW_USER_WITH_PWD', 'surname' : 'SURNAME', 'username' : 'NEW_USER_WITH_PWD', 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'MOB1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'status' : 'active'  } ]
        json_user_pwd = self._assert_req('/add/user', user_data_pwd, { 'error' : None, 'ids' : [ '' ] })
        id_user_pwd = json_user_pwd['ids'][0]
        
        # Add one user with status != active, should not login
        user_data_inactive = [ { 'name' : 'NEW_USER_INACTIVE', 'surname' : 'SURNAME', 'username' : 'NEW_USER_INACTIVE', 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'MOB1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [], 'status' : 'disabled'  } ]
        json_user_inactive = self._assert_req('/add/user', user_data_inactive, { 'error' : None, 'ids' : [ '' ] })
        id_user_inactive = json_user_inactive['ids'][0]
        
        user_data_nopwd = [ { 'name' : 'NEW_USER_WITH_NO_PWD', 'surname' : 'SURNAME', 'username' : 'NEW_USER_WITH_NO_PWD', 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'MOB1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : '', 'salt' : 'RANDOM_UNUSED_SALT', 'salary' : [], 'status' : 'active'  } ]
        # Add user without password, should raise error
        self._assert_req('/add/user', user_data_nopwd, { 'error' : "ValidationError: u'' is too short", 'ids' : [ ] })
         
        # Check if can't login with NEW_USER_WITH_NO_PWD
        self._login(user_data_nopwd[0], 'employee')
        self._assert_unlogged()
        
        # Check if can login with NEW_USER_WITH_PWD
        self._login(user_data_pwd[0], 'employee')
        self._assert_logged(user_data_pwd[0])

        # Check if can login with NEW_USER_INACTIVE
        self._login(user_data_inactive[0], 'employee')
        self._assert_unlogged()
         
        # Delete the inserted user
        self.execOnTearDown.append(('/remove/user', [ { '_id' :  id_user_pwd }, { '_id' :  id_user_inactive } ], { 'error' : None }))
         
 
class DayAPIAsEmployee(TestCaseAsEmployee):
     
    def test_day_ok(self):
         
        # Get itself
        self._assert_req('/get/user', [ { '_id' : self.employee_id }, { '_id' : 1 }, { } ], { 'error': None, 'records' : [ { '_id' : '' } ] })
  
        # Update itself
        self._assert_req('/update/user', { '_id' : self.employee_id, 'email' : 'CHANGEDEMAIL@DOMAIN.COM' }, { 'error': None })
        self._assert_req('/get/user', [ { '_id' : self.employee_id }, { 'email' : 1, '_id' : 0 }, { } ], { 'error': None, 'records' : [ { 'email' : 'CHANGEDEMAIL@DOMAIN.COM' } ] })
        self._assert_req('/update/user', { '_id' : self.employee_id, 'email' : 'EMAIL@DOMAIN.COM' }, { 'error': None })
         
  
    def test_day_ko(self):
  
        # Get admin
        self._assert_req('/get/user', [ { '_id' : '1'*24 }, { '_id' : 1 }, { } ], { 'error': "ValidationError: u'111111111111111111111111' does not match '^%s$'" % (self.employee_id), 'records' : [ ] })
  
        # Get its private fields
        self._assert_req('/get/user', [ { '_id' : self.employee_id }, { 'password' : 1 }, { } ], { 'error': "TSValidationError: Field 'get.user.password' is restricted for current user", 'records' : [ ] })
        self._assert_req('/get/user', [ { '_id' : self.employee_id }, { 'salt' : 1 }, { } ], { 'error': "TSValidationError: Field 'get.user.salt' is restricted for current user", 'records' : [ ] })
        self._assert_req('/get/user', [ { '_id' : self.employee_id }, { 'status' : 1 }, { } ], { 'error': "TSValidationError: Field 'get.user.status' is restricted for current user", 'records' : [ ] })
        self._assert_req('/get/user', [ { '_id' : self.employee_id }, { 'contract' : 1 }, { } ], { 'error': "TSValidationError: Field 'get.user.contract' is restricted for current user", 'records' : [ ] })
  
        # Update private fields
        # TODO: restrict this
        # self._assert_req('/update/user', { '_id' : self.employee_id, 'status' : 'active' }, { 'error': "none" })
   
        # Wrong email type
        self._assert_req('/update/user', { '_id' : self.employee_id, 'email' : 'CHANGEDEMAIL#DOMAIN.COM' }, {u'error': u"ValidationError: u'CHANGEDEMAIL#DOMAIN.COM' is not a 'email'"})
         
        # Delete himself
        self._assert_req('/remove/user', [ {  '_id' : self.employee_id } ], { 'error': "TSValidationError: Access to 'remove.user' is restricted for current user" })
  

class DayAPIAsManager(TestCaseAsManager):
    
    def test_day_ok(self):
        
        # Get itself
        self._assert_req('/get/user', [ { '_id' : self.manager_id }, { '_id' : 1 }, { } ], { 'error': None, 'records' : [ { '_id' : '' } ] })
 
        # Update itself
        self._assert_req('/update/user', { '_id' : self.manager_id, 'email' : 'NEWEMAIL@NEWDOMAIN.COM' }, { 'error': None })
        self._assert_req('/get/user', [ { '_id' : self.manager_id }, { 'email' : 1, '_id' : 0 }, { } ], { 'error': None, 'records' : [ { 'email' : 'NEWEMAIL@NEWDOMAIN.COM' } ] })
        self._assert_req('/update/user', { '_id' : self.manager_id, 'email' : 'EMAIL@DOMAIN.COM' }, { 'error': None })

        # Get admin
        self._assert_req('/get/user', [ { '_id' : '1'*24 }, { '_id' : 1 }, { } ], { 'error': None, 'records' : [ { '_id' : '' } ] })
                
 
    def test_day_ko(self):
        
        # Get admin salary
        self._assert_req('/get/user', [ { '_id' : '1'*24 }, { 'salary' : 1 }, { } ], { 'error': "TSValidationError: Field 'get.user.salary' is restricted for current user", 'records' : [ ] })
        
        # Get its private fields
        self._assert_req('/get/user', [ { '_id' : self.manager_id }, { 'password' : 1 }, { } ], { 'error': "TSValidationError: Field 'get.user.password' is restricted for current user", 'records' : [ ] })
        self._assert_req('/get/user', [ { '_id' : self.manager_id }, { 'salt' : 1 }, { } ], { 'error': "TSValidationError: Field 'get.user.salt' is restricted for current user", 'records' : [ ] })
        self._assert_req('/get/user', [ { '_id' : self.manager_id }, { 'status' : 1 }, { } ], { 'error': "TSValidationError: Field 'get.user.status' is restricted for current user", 'records' : [ ] })
        self._assert_req('/get/user', [ { '_id' : self.manager_id }, { 'contract' : 1 }, { } ], { 'error': "TSValidationError: Field 'get.user.contract' is restricted for current user", 'records' : [ ] })

        # Update private fields
        # TODO: restrict this
        # self._assert_req('/update/user', { '_id' : self.manager_id, 'status' : 'active' }, { 'error': "none" })

        # Delete himself
        self._assert_req('/remove/user', [ {  '_id' : self.manager_id } ], { 'error': "TSValidationError: Access to 'remove.user' is restricted for current user" })
 
 