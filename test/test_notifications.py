from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager, admin_credentials

class ModuleData:

    def _add_module_data(self, current_id):
        
        # Add two elements USERTEST1 and USERTEST2
        users_json = self._assert_req('/add/user', [ 
                                                    { 'name' : 'USERTEST1', 'surname' : 'SURNAME', 'username' : 'USERNAME1' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [ { 'cost' : 5, 'from': '2004-01-02', 'to' : '2006-01-02' }], 'status' : 'active'  }, 
                                                    ], { 'error' : None, 'ids' : [ '' ] })
        self.users_ids = users_json['ids'] 
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.users_ids[0]  } ], { 'error' : None }))
        
        # Add projects
        projects_json = self._assert_req('/add/project', [ 
                                 { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE1' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag1', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[0], 'name' : 'Emp1'} ], 
                                  'expences' : [ 
                                                 { '_id' : '6'*24, "user_id" : '1'*24, "trip_id" : '3'*24, 'status' : 2, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2005-10-04', 'amount' : 5}, { 'date' : '2000-01-05', 'amount' : 10}] },
                                                 { '_id' : '5'*24, "user_id" : current_id, "trip_id" : '4'*24, 'status' : 3, "date" : "2010-10-09", "file" : {}, 'objects' : [{ 'date' : '2005-10-09', 'amount' : 5}, { 'date' : '2000-01-09', 'amount' : 10}] }     
                                 ]
                                   
                                   },
                                 { 'customer' : 'CUSTOMER1', 'tags' : [ 'TYPE2' ], 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag2', 'role' : 'project manager'} ], 'employees' : [ { '_id' : current_id, 'name' : 'Emp2'} ], 
                                  'expences' : [ 
                                                 { '_id' : '7'*24, "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 2, "date" : "2010-10-07", "file" : {}, 'objects' : [{ 'date' : '2003-04-10', 'amount' : 15}, { 'date' : '2005-01-05', 'amount' : 20}] },     
                                                 { '_id' : '8'*24, "user_id" : current_id, "trip_id" : '2'*24, 'status' : 3, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2009-01-04', 'amount' : 7}] }     
                                 ] 
                                   }, 
                                 { 'customer' : 'CUSTOMER3', 'tags' : [ 'TYPE3' ], 'name' : 'PROJECTNAME3', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag3', 'role' : 'project manager'} ], 'employees' : [ { '_id' : current_id, 'name' : 'Emp3'} ],
                                  'trips' : [ 
                                                 { '_id' : '8'*24, "user_id" : '1'*24, "description" : "trip1", "status" : 0, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },     
                                                 { '_id' : '9'*24, "user_id" : current_id, "description" : "trip2", "status" : 2, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },    
                                                 { '_id' : '3'*24, "user_id" : current_id, "description" : "trip3", "status" : -2, "start" : "2010-10-10", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} }     
                                 ] } 
                                 ], 
                { 'error' : None, 'ids' : [ '', '', '' ] }
                )
        self.projects_ids = projects_json['ids']

        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }, { '_id' : self.projects_ids[1] }, { '_id' : self.projects_ids[2] }  ], { 'error' : None }))
 

  
class ApprovalAPIAsAdmin(TestClassBase, ModuleData):
      
  
    def setUp(self):        
        TestClassBase.setUp(self)
        ModuleData._add_module_data(self, '1'*24)

    def test_notifications_ok(self):
        
        self._assert_logged(self.admin_data[0],  5)


class ApprovalAPIAsManager(TestCaseAsManager, ModuleData):
      
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.manager_id)
        self._log_as_user()

    def test_notifications_ok(self):
 
        # Manager has 3 pending notifications 
        self._assert_logged(self.manager_data[0],  3)
 

class ApprovalAPIAsUser(TestCaseAsEmployee, ModuleData):
      
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.employee_id)
        self._log_as_user()
 
    def test_notifications_ok(self):
 
        # Employee has 2 pending notifications 
        self._assert_logged(self.employee_data[0],  2)
 
