from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager
from core.config import conf_approval_flow
from core.validation.permissions import get_role_approval_step

class ModuleData:

    def _add_module_data(self, current_id):
        
        # Add two elements USERTEST1 and USERTEST2
        users_json = self._assert_req('/add/user', [ 
                                                    { 'name' : 'USERTEST1', 'surname' : 'SURNAME', 'username' : 'USERNAME1' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [ { 'cost' : 5, 'from': '2004-01-02', 'to' : '2006-01-02' }], 'status' : 'active'  }, 
                                                    { 'name' : 'USERTEST2', 'surname' : 'SURNAME', 'username' : 'USERNAME2' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER2', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : [ { 'cost' : 10, 'from': '2004-01-02', 'to' : '2010-01-02' }], 'status' : 'active'  }, 
                                                    { 'name' : 'USERTEST3', 'surname' : 'SURNAME', 'username' : 'USERNAME3' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER3', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : [ { 'cost' : 100, 'from': '2000-01-02', 'to' : '2010-01-02' }], 'status' : 'active'  } 
                                                    ], { 'error' : None, 'ids' : [ '', '', '' ] })
        self.users_ids = users_json['ids'] 
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.users_ids[0]  }, { '_id' : self.users_ids[1]  }, { '_id' : self.users_ids[2] } ], { 'error' : None }))
        
        # Add projects
        projects_json = self._assert_req('/add/project', [ 
                                 { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE'  ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag1', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ], 
                                  'expences' : [ 
                                                 { '_id' : '7'*24, "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 0, "date" : "2010-10-08", "file" : {}, 'objects' : [{}] },     
                                                 { '_id' : '8'*24, "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 1, "date" : "2010-10-08", "file" : {}, 'objects' : [{}] }     
                                 ] }, 
                                 { 'customer' : 'CUSTOMER1', 'tags' : [ 'TYPE'  ], 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : '1'*24, 'name' : 'Manag2', 'role' : 'project manager'} ], 'employees' : [ { '_id' : current_id, 'name' : 'Emp2'} ] }, 
                                 { 'customer' : 'CUSTOMER3', 'tags' : [ 'TYPE'  ], 'name' : 'PROJECTNAME3', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : '1'*24, 'name' : 'Manag3', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[2], 'name' : 'Emp3'} ] } 
                                 ], 
                { 'error' : None, 'ids' : [ '', '', '' ] }
                )
        self.projects_ids = projects_json['ids']

        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }, { '_id' : self.projects_ids[1] }, { '_id' : self.projects_ids[2] }  ], { 'error' : None }))
 

  
class ExpencesAPIAsAdmin(TestClassBase, ModuleData):
      
  
    def setUp(self):        
        TestClassBase.setUp(self)
        ModuleData._add_module_data(self, '1'*24)
    

    def test_expences_search(self):

        self.maxDiff = None         
        # Search by project id
        self._assert_req('/data/search_expences', { 'project_id':  self.projects_ids[0]  }, {u'error': None, 'records' : [
                                                 { '_id' : '', 'project_id':  self.projects_ids[0],  "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 1, "date" : "2010-10-08", "file" : {}, 'objects' : [{}] },     
                                                 { '_id' : '', 'project_id':  self.projects_ids[0], "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 0, "date" : "2010-10-08", "file" : {}, 'objects' : [{}] }     
                                 ]})
         
        # Filter by status
        self._assert_req('/data/search_expences', { 'project_id':  self.projects_ids[0], 'status' : [1]  }, {u'error': None, 'records' : [
                                                 { '_id' : '', 'project_id':  self.projects_ids[0], "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 1, "date" : "2010-10-08", "file" : {}, 'objects' : [{}] }     
                                 ]})
         
         
 
    def test_expences_ok(self):
        
         # Insert one expence
         self._assert_req('/data/push_expences', [ 
                                 { '_id' : self.projects_ids[0], 
                                  "expences" : [ 
                                                 { "user_id" : '1'*24, "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }     
                                 ] } ], 
                { 'error' : None, 'ids' : [ '' ] }
                )
         
         
 
         # Insert more expences in the same project
         self._assert_req('/data/push_expences', [ 
                                 { '_id' : self.projects_ids[0], 
                                  "expences" : [ 
                                                 { "user_id" : self.users_ids[1], "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                                 { "user_id" : self.users_ids[2], "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }     
                                 ] } ], 
                { 'error' : None, 'ids' : [ '', '' ] }
                )

         # Get inserted expences
         self._assert_req('/data/search_expences', { "user_id" : self.users_ids[1] }, { 'error' : None, 'records' : [ 
                                                 { '_id' : '', 'project_id':  self.projects_ids[0], "user_id" : self.users_ids[1], "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                               ]})

         self.maxDiff = None
         # Get all inserted expences
         found_expences = self._assert_req('/data/search_expences', { "project_id" : self.projects_ids[0], 'start' : '2005-09-09', 'end' : '2005-10-10' }, { 'error' : None, 'records' : [ 
                                                 { '_id' : '', 'project_id':  self.projects_ids[0], "user_id" : self.users_ids[2], "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },     
                                                 { '_id' : '', 'project_id':  self.projects_ids[0], "user_id" : self.users_ids[1], "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                                 { '_id' : '', 'project_id':  self.projects_ids[0], "user_id" : '1'*24, "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }     
                                               ]})
    
        # Delete one expence
         self._assert_req('/data/push_expences', [ 
                               { '_id' : self.projects_ids[0], 
                                "expences" : [ { '_id' : found_expences['records'][0]['_id'] } ] } ], 
              { 'error' : None, 'ids' : [ '' ] }
          )

         self._assert_req('/data/search_expences', { "project_id" : self.projects_ids[0], 'start' : '2005-09-09', 'end' : '2005-10-10' }, { 'error' : None, 'records' : [ 
                                                 { '_id' : '', 'project_id':  self.projects_ids[0], "user_id" : self.users_ids[1], "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                                 { '_id' : '', 'project_id':  self.projects_ids[0], "user_id" : '1'*24, "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }     
                                               ]})
    
class ExpencesAPIAsEmployee(TestCaseAsEmployee, ModuleData):
    
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.employee_id)
        self._log_as_user()
        
        
    def test_expences_ok(self):

        # Insert one trip in a project where user works
        self._assert_req('/data/push_expences', [ 
                                { '_id' : self.projects_ids[1], 
                                 "expences" : [ 
                                                 { "user_id" : self.employee_id, "trip_id" : '2'*24, 'status': get_role_approval_step('draft'), "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                ] } ], 
               { 'error' : None, 'ids' : [ '' ] }
       )

        self._assert_req('/data/search_expences', { "user_id" : self.employee_id,  "employee_id" : self.employee_id }, {u'error': None, 'records' : [{ '_id' : '', "user_id" : self.employee_id, 'project_id' : self.projects_ids[1], "trip_id" : '2'*24, 'status' : get_role_approval_step('draft'), "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }]})
        
        
    def test_expences_ko(self):
        
        # Insert one expence in unknown project
        self._assert_req('/data/push_expences', [ 
                                { '_id' : '7'*24, 
                                 "expences" : [ 
                                                 { "user_id" : self.employee_id, "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                ] } ], 
               { 'error' : "TSValidationError: Access to project '%s' is restricted for current user" % ('7'*24) }
               )          
        
        # Insert one expence in project where user does not work 
        self._assert_req('/data/push_expences', [ 
                                { '_id' : self.projects_ids[2], 
                                 "expences" : [ 
                                                 { "user_id" : self.employee_id, "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                ] } ], 
               { 'error' : "TSValidationError: Access to project '%s' is restricted for current user" % (self.projects_ids[2]) }
               )       

        # Insert a trip in correct project with wrong user_id
        self.maxDiff = None
        self._assert_req('/data/push_expences', [ 
                                 { '_id' : self.projects_ids[1], 
                                  "expences" : [ 
                                                 { "user_id" : self.users_ids[1], "trip_id" : '2'*24, 'status': get_role_approval_step('draft'), "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                 ] } ], 
                {u'error': u"ValidationError: u'%s' does not match '^%s$'" % (self.users_ids[1], self.employee_id)}
        )

        # Search without specify ids
        self._assert_req('/data/search_expences', {  }, {u'error': u"ValidationError: 'employee_id' is a required property"})
         
        # Search with wrong ids
        self._assert_req('/data/search_expences', { "user_id" : self.users_ids[1],  "employee_id" : self.users_ids[1] }, {u'error': u"ValidationError: u'%s' does not match '^%s$'" % (self.users_ids[1], self.employee_id)})
 
         

class ExpencesAPIAsManager(TestCaseAsManager, ModuleData):
     
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.manager_id)
        self._log_as_user()

    def test_expences_ok(self):

        # Insert one trip in a project where user works
        self._assert_req('/data/push_expences', [ 
                                { '_id' : self.projects_ids[1], 
                                 "expences" : [ 
                                                 { "user_id" : self.manager_id, "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                ] } ], 
               { 'error' : None, 'ids' : [ '' ] }
       )

        # Insert one trip in a project administrated by user
        self._assert_req('/data/push_expences', [ 
                                { '_id' : self.projects_ids[0], 
                                 "expences" : [ 
                                                 { "user_id" : self.manager_id, "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                ] } ], 
               { 'error' : None, 'ids' : [ '' ] }
       )


        # Insert a trip in correct project with different user_id (project manager can)
        self.maxDiff = None
        self._assert_req('/data/push_expences', [ 
                                 { '_id' : self.projects_ids[0], 
                                  "expences" : [ 
                                                 { "user_id" : self.users_ids[1], "trip_id" : '2'*24, 'status': 0, "date" : "2000-10-08", "file" : {}, 'objects' : [{}] },   
                                 ] } ], 
               { 'error' : None, 'ids' : [ '' ] }
        )          

        # Search only last trip specifying time stamp
        self._assert_req('/data/search_expences', {  "responsible_id" : self.manager_id, 'start' : '1999-01-01', 'end' : '2001-10-08' }, {u'error': None, 'records' : [{ '_id' : '', 'project_id' : self.projects_ids[0], "user_id" : self.users_ids[1], "trip_id" : '2'*24, 'status': 0, "date" : "2000-10-08", "file" : {}, 'objects' : [{}] }]})
 
        # Search by employee_id
        self._assert_req('/data/search_expences', {  "employee_id" : self.manager_id }, {u'error': None, 'records' : [{ '_id' : '', "user_id" : self.manager_id, 'project_id' : self.projects_ids[1], "trip_id" : '2'*24, 'status': 0, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }]})
        
 
         
    def test_day_ko(self):
        self.maxDiff = None
        # Insert one expence in an unknown project 
        self._assert_req('/data/push_expences', [ 
                                { '_id' : '7'*24, 
                                 "expences" : [ 
                                                 { "user_id" : self.users_ids[0], "trip_id" : '2'*24, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                ] } ], 
               { u'error' : u"ValidationError: u'%s' is not one of %s" % ('7'*24, [ str(self.projects_ids[1]), str(self.projects_ids[0]) ]) }
        )    
        
        # Insert one expence in project where user does not work 
        self._assert_req('/data/push_expences', [ 
                                { '_id' : self.projects_ids[2], 
                                 "expences" : [ 
                                                 { "user_id" : self.manager_id, "trip_id" : '2'*24, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] },   
                                ] } ], 
               { u'error' : u"ValidationError: u'%s' is not one of %s" % (self.projects_ids[2], [ str(self.projects_ids[1]), str(self.projects_ids[0]) ]) }
               )       

        # Insert a trip in a not administrated project (this should fail) TODO: fix this
#         self._assert_req('/data/push_expences', [ 
#                                  { '_id' : self.projects_ids[1], 
#                                   "expences" : [ 
#                                                   { "user_id" : self.users_ids[1], "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'note' : 'too expensive', 'accommodation' : {} }     
#                                  ] } ], 
#                 {u'error': u"ValidationError: {u'status': 2, u'city': u'Austin', u'user_id': u'%s', u'description': u'descr2', u'country': u'USA', u'note': u'too expensive', u'start': u'2009-10-08', u'end': u'2009-10-10', u'accommodation': {}} is not valid under any of the given schemas" % (self.users_ids[1])}
#         )     


        # Search without specify ids
        self._assert_req('/data/search_expences', {  }, {u'error': u"ValidationError: {} is not valid under any of the given schemas"})
          
        # Search with wrong ids
        self._assert_req('/data/search_expences', {  "responsible_id" : self.users_ids[1] }, {u'error': u"ValidationError: {u'responsible_id': u'%s'} is not valid under any of the given schemas" % (self.users_ids[1])})
  
         
         
         