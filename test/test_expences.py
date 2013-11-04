from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager

class ModuleData:

    def _add_module_data(self, current_id):
        
        # Add two elements USERTEST1 and USERTEST2
        users_json = self._assert_req('/add/user', [ 
                                                    { 'name' : 'USERTEST1', 'surname' : 'SURNAME', 'username' : 'USERNAME1' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [ { 'cost' : 5, 'from': '2004-01-02', 'to' : '2006-01-02' }]  }, 
                                                    { 'name' : 'USERTEST2', 'surname' : 'SURNAME', 'username' : 'USERNAME2' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER2', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : [ { 'cost' : 10, 'from': '2004-01-02', 'to' : '2010-01-02' }]  }, 
                                                    { 'name' : 'USERTEST3', 'surname' : 'SURNAME', 'username' : 'USERNAME3' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER3', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : [ { 'cost' : 100, 'from': '2000-01-02', 'to' : '2010-01-02' }]  } 
                                                    ], { 'error' : None, 'ids' : [ '', '', '' ] })
        self.users_ids = users_json['ids'] 
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.users_ids[0]  }, { '_id' : self.users_ids[1]  }, { '_id' : self.users_ids[2] } ], { 'error' : None }))
        
        # Add projects
        projects_json = self._assert_req('/add/project', [ 
                                 { 'customer' : 'CUSTOMER', 'type' : 'TYPE', 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsible' : { '_id' : current_id, 'name' : 'Manag1'}, 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ], 
                                  'expences' : [ 
                                                 { '_id' : '7'*24, "user_id" : '1'*24, "trip_id" : '2'*24, "date" : "2010-10-08", "file" : {}, 'objects' : [{}] }     
                                 ] }, 
                                 { 'customer' : 'CUSTOMER1', 'type' : 'TYPE', 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsible' : { '_id' : current_id, 'name' : 'Manag2'}, 'employees' : [ { '_id' : self.users_ids[0], 'name' : 'Emp2'} ] }, 
                                 { 'customer' : 'CUSTOMER3', 'type' : 'TYPE', 'name' : 'PROJECTNAME3', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsible' : { '_id' : '1'*24, 'name' : 'Manag3'}, 'employees' : [ { '_id' : self.users_ids[2], 'name' : 'Emp3'} ] } 
                                 ], 
                { 'error' : None, 'ids' : [ '', '', '' ] }
                )
        self.projects_ids = projects_json['ids']

        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }, { '_id' : self.projects_ids[1] }, { '_id' : self.projects_ids[2] }  ], { 'error' : None }))
 

  
class ExpencesAPIAsAdmin(TestClassBase, ModuleData):
      
  
    def setUp(self):        
        TestClassBase.setUp(self)
        ModuleData._add_module_data(self, '1'*24)
      
    def test_expences_ok(self):
        
         # Insert one expence
         self._assert_req('/data/push_expences', [ 
                                 { '_id' : self.projects_ids[0], 
                                  "expences" : [ 
                                                 { "user_id" : '1'*24, "trip_id" : '2'*24, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }     
                                 ] } ], 
                { 'error' : None, 'ids' : [ '' ] }
                )
         
         
 
         # Insert more expences in the same project
         self._assert_req('/data/push_expences', [ 
                                 { '_id' : self.projects_ids[0], 
                                  "expences" : [ 
                                                 { "user_id" : self.users_ids[1], "trip_id" : '2'*24, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                                 { "user_id" : self.users_ids[2], "trip_id" : '2'*24, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }     
                                 ] } ], 
                { 'error' : None, 'ids' : [ '', '' ] }
                )

         # Get inserted expences
         self._assert_req('/get/project', [ { '_id' : self.projects_ids[0] }, { '_id' : 0, 'expences._id' : 1 }] , {u'error': None, u'records': [{u'expences': [{u'_id': ''}, {u'_id': ''}, {u'_id': ''}, {u'_id': ''}]}]} )
         