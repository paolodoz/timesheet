from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager
from core.config import conf_approval_flow

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
                                 { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag1', 'role' : 'project manager' } ], 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ], 
                                  'trips' : [ 
                                                 { '_id' : '7'*24, "user_id" : '1'*24, "description" : "descr1", "status" : 0, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} }     
                                 ] }, 
                                 { 'customer' : 'CUSTOMER1', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : '1'*24, 'name' : 'Manag2', 'role' : 'project manager' } ], 'employees' : [ { '_id' :current_id, 'name' : 'Emp2'} ], 'trips' : [ 
                                                 { '_id' : '8'*24, "user_id" : '1'*24, "description" : "descr1", "status" : 0, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },     
                                                 { '_id' : '9'*24, "user_id" : current_id, "description" : "descr1", "status" : 1, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} }     
                                 ] }, 
                                 { 'customer' : 'CUSTOMER3', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME3', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : '1'*24, 'name' : 'Manag3', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[2], 'name' : 'Emp3'} ] } 
                                 ], 
                { 'error' : None, 'ids' : [ '', '', '' ] }
                )
        self.projects_ids = projects_json['ids']

        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }, { '_id' : self.projects_ids[1] }, { '_id' : self.projects_ids[2] }  ], { 'error' : None }))
 

  
class TripsAPIAsAdmin(TestClassBase, ModuleData):
      
  
    def setUp(self):        
        TestClassBase.setUp(self)
        ModuleData._add_module_data(self, '1'*24)



    def test_trips_search(self):
         
        # Search by project id
        self._assert_req('/data/search_trips', { 'project_id':  self.projects_ids[1]  }, {u'error': None, 'records' : [
                                                 { '_id' : '', 'project_id':  self.projects_ids[1], "user_id" : '1'*24, "description" : "descr1", "status" : 1, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },     
                                                 { '_id' : '', 'project_id':  self.projects_ids[1], "user_id" : '1'*24, "description" : "descr1", "status" : 0, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} }     
                                 ]})
         
        # Filter by status
        self._assert_req('/data/search_trips', { 'project_id':  self.projects_ids[1], 'status' : [1]  }, {u'error': None, 'records' : [
                                                 { 'project_id':  self.projects_ids[1], '_id' : '', "user_id" : '1'*24, "description" : "descr1", "status" : 1, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },     
                                 ]})
         
        # Search by trip_id
        self._assert_req('/data/search_trips', { 'trip_id':  '7'*24  }, {u'error': None, 'records' : [
                                                 { 'project_id':  self.projects_ids[0], '_id' : '', "user_id" : '1'*24, "description" : "descr1", "status" : 0, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },     
                                 ]})
        
         
      
    def test_trips_ok(self):
        
         
        # Insert one expence
        self._assert_req('/data/push_trips', [ 
                                { '_id' : self.projects_ids[0], 
                                 "trips" : [ 
                                                 { "user_id" : self.users_ids[0], "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }     
                                ] } ], 
               { 'error' : None, 'ids' : [ '' ] }
               )
 
        # Insert more trips in the same project
        self._assert_req('/data/push_trips', [ 
                                { '_id' : self.projects_ids[0], 
                                 "trips" : [ 
                                                 { "user_id" : self.users_ids[0], "description" : "descr3", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} },     
                                                 { "user_id" : self.users_ids[1], "description" : "descr4", "status" : 0, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "Austria", 'city' : "Wien", 'notes' : [ 'approved' ], 'accommodation' : {} }     
                                ] } ], 
               { 'error' : None, 'ids' : [ '', '' ] }
               )
 

        # Get inserted trip
        found_trips = self._assert_req('/data/search_trips', { "user_id" : self.users_ids[0] }, { 'error' : None, 'records' : [ 
                                                 { 'project_id':  self.projects_ids[0],  '_id' : '', "user_id" : self.users_ids[0], "description" : "descr3", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", u'city' : "Austin", u'notes' :  [ u'too expensive' ], u'accommodation' : {} },     
                                                 { 'project_id':  self.projects_ids[0], '_id' : '', "user_id" : self.users_ids[0], "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", u'city' : "Austin", u'notes' :  [ u'too expensive' ], u'accommodation' : {} }     
                                               ]})
    
        # Delete one trip
        self._assert_req('/data/push_trips', [ 
                                { '_id' : self.projects_ids[0], 
                                 "trips" : [ { '_id' : found_trips['records'][0]['_id'] } ] } ], 
               { 'error' : None, 'ids' : [ '' ] }
           )
    
        # Re-Get inserted trip
        self.maxDiff = None
        found_trips = self._assert_req('/data/search_trips', { "user_id" : self.users_ids[0] }, { 'error' : None, 'records' : [ 
                                                 { 'project_id':  self.projects_ids[0], '_id' : '', "user_id" : self.users_ids[0], "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", u'city' : "Austin", u'notes' :  [ u'too expensive' ], u'accommodation' : {} }     
                                               ]})    
    
class TripAPIAsEmployee(TestCaseAsEmployee, ModuleData):
    
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.employee_id)
        self._log_as_user()


    def test_trips_search(self):
         
        self._assert_req('/data/search_trips', { 'user_id':self.employee_id, "employee_id" : self.employee_id }, {u'error': None, 'records' : [
                                                                                                                    { 'project_id':  self.projects_ids[1], '_id' : '', "user_id" : self.employee_id, "description" : "descr1", "status" : 1, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} }
                                                                                                                    ]})
                 
        
    def test_trips_ok(self):

        # Insert one trip in a project where user works
        self._assert_req('/data/push_trips', [ 
                                { '_id' : self.projects_ids[1], 
                                 "trips" : [ 
                                                 { "user_id" : self.employee_id, "description" : "descr2", "status" : conf_approval_flow.index('draft'), "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'draft' ], 'accommodation' : {} }     
                                ] } ], 
               { 'error' : None, 'ids' : [ '' ] }
       )
        
        self._assert_req('/data/search_trips', { "user_id" : self.employee_id,  "employee_id" : self.employee_id }, {u'error': None, 'records' : [{ '_id' : '', 'project_id' : self.projects_ids[1],  "user_id" : self.employee_id, "description" : "descr2", "status" : conf_approval_flow.index('draft'), "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'draft' ], 'accommodation' : {} },
                                                                                                                                                  { '_id' : '', 'project_id' : self.projects_ids[1], "user_id" : self.employee_id, "description" : "descr1", "status" : 1, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} }     

                                                                                                                                                  
                                                                                                                                                  ]})

         
         
    def test_trips_ko(self):
         
        # Insert one expence in unknown project
        self._assert_req('/data/push_trips', [ 
                                { '_id' : '7'*24, 
                                 "trips" : [ 
                                                 { "user_id" : self.employee_id, "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }     
                                ] } ], 
               { 'error' : "TSValidationError: Access to project '%s' is restricted for current user" % ('7'*24) }
               )          
         
        # Insert one expence in project where user does not work 
        self._assert_req('/data/push_trips', [ 
                                { '_id' : self.projects_ids[2], 
                                 "trips" : [ 
                                                 { "user_id" : self.employee_id, "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }     
                                ] } ], 
               { 'error' : "TSValidationError: Access to project '%s' is restricted for current user" % (self.projects_ids[2]) }
               )       
 
        # Insert a trip in correct project with wrong user_id
        self.maxDiff = None
        self._assert_req('/data/push_trips', [ 
                                 { '_id' : self.projects_ids[1], 
                                  "trips" : [ 
                                                  { "user_id" : self.users_ids[1], "description" : "descr2", "status" : conf_approval_flow.index('draft'), "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }     
                                 ] } ], 
                                 {u'error': u"ValidationError: u'%s' does not match '^%s$'" % (self.users_ids[1], self.employee_id)}
                                 )
        # Search without specify ids
        self._assert_req('/data/search_trips', {  }, {u'error': u"ValidationError: 'employee_id' is a required property"})
         
        # Search with wrong ids
        self._assert_req('/data/search_trips', { "user_id" : self.users_ids[1],  "employee_id" : self.users_ids[1] }, {u'error': u"ValidationError: u'%s' does not match '^%s$'" % (self.users_ids[1], self.employee_id)})
 
 
class TripAPIAsManager(TestCaseAsManager, ModuleData):
      
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.manager_id)
        self._log_as_user()
 
    def test_trips_search(self):
         
        # Search trips by responsible
        self._assert_req('/data/search_trips', {  "responsible_id" : self.manager_id }, {u'error': None, 'records' : [
                                                                                                                    { 'project_id':  self.projects_ids[0], '_id' : '', "user_id" : '1'*24, "description" : "descr1", "status" : 0, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} } 
                                                                                                                    ]})
 
        # Search trips by employee
 
        self._assert_req('/data/search_trips', {  "employee_id" : self.manager_id }, {u'error': None, 'records' : [
                                                 { 'project_id':  self.projects_ids[1], '_id' : '', "user_id" : self.manager_id, "description" : "descr1", "status" : 1, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },
                                                 
                                                 { 'project_id':  self.projects_ids[1], '_id' : '', "user_id" : '1'*24, "description" : "descr1", "status" : 0, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },     
                                                                                                               ]})
 
 
    def test_trips_ok(self):
 
        # Insert one trip in a project where user works
        self._assert_req('/data/push_trips', [ 
                                { '_id' : self.projects_ids[1], 
                                 "trips" : [ 
                                                 { "user_id" : self.manager_id, "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }     
                                ] } ], 
               { 'error' : None, 'ids' : [ '' ] }
       )
 
        # Insert one trip in a project administrated by user
        self._assert_req('/data/push_trips', [ 
                                { '_id' : self.projects_ids[0], 
                                 "trips" : [ 
                                                 { "user_id" : self.manager_id, "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }     
                                ] } ], 
               { 'error' : None, 'ids' : [ '' ] }
       )
 
 
        # Insert a trip in correct project with different user_id (project manager can)
        self.maxDiff = None
        self._assert_req('/data/push_trips', [ 
                                 { '_id' : self.projects_ids[0], 
                                  "trips" : [ 
                                                  { "user_id" : self.users_ids[1], "description" : "descr2", "status" : 2, "start" : "2000-10-08", "end" : "2000-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }     
                                 ] } ], 
               { 'error' : None, 'ids' : [ '' ] }
        )   
        
        # Search only last trip specifying time stamp
        self._assert_req('/data/search_trips', {  "responsible_id" : self.manager_id, 'start' : '1999-01-01', 'end' : '2001-10-08' }, {u'error': None, 'records' : [{ 'project_id':  self.projects_ids[0], '_id' : '',  "user_id" : self.users_ids[1], "description" : "descr2", "status" : 2, "start" : "2000-10-08", "end" : "2000-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }]})
       
          
    def test_trips_ko(self):
        self.maxDiff = None
        # Insert one expence in an unknown project 
        self._assert_req('/data/push_trips', [ 
                                { '_id' : '7'*24, 
                                 "trips" : [ 
                                                 { "user_id" : self.users_ids[0], "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }     
                                ] } ], 
               { u'error' : u"ValidationError: u'%s' is not one of %s" % ('7'*24, [ str(self.projects_ids[1]), str(self.projects_ids[0]) ]) }
        )    
         
        # Insert one expence in project where user does not work 
        self._assert_req('/data/push_trips', [ 
                                { '_id' : self.projects_ids[2], 
                                 "trips" : [ 
                                                 { "user_id" : self.manager_id, "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }     
                                ] } ], 
               { u'error' : u"ValidationError: u'%s' is not one of %s" % (self.projects_ids[2], [ str(self.projects_ids[1]), str(self.projects_ids[0]) ]) }
               )       
 
        # Insert a trip in a not administrated project (this should fail) TODO: fix this
#         self._assert_req('/data/push_trips', [ 
#                                  { '_id' : self.projects_ids[1], 
#                                   "trips" : [ 
#                                                   { "user_id" : self.users_ids[1], "description" : "descr2", "status" : 2, "start" : "2009-10-08", "end" : "2009-10-10", "country" : "USA", 'city' : "Austin", 'notes' : [ 'too expensive' ], 'accommodation' : {} }     
#                                  ] } ], 
#                 {u'error': u"ValidationError: {u'status': 2, u'city': u'Austin', u'user_id': u'%s', u'description': u'descr2', u'country': u'USA', u'notes': [ u'too expensive' ], u'start': u'2009-10-08', u'end': u'2009-10-10', u'accommodation': {}} is not valid under any of the given schemas" % (self.users_ids[1])}
#         )       

        # Search without specify ids
        self._assert_req('/data/search_trips', {  }, {u'error': u"ValidationError: {} is not valid under any of the given schemas"})
          
        # Search with wrong ids
        self._assert_req('/data/search_trips', {  "responsible_id" : self.users_ids[1] }, {u'error': "ValidationError: {u'responsible_id': u'%s'} is not valid under any of the given schemas" % (self.users_ids[1])})
  
    