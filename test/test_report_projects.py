from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager

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
                                 { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE1' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag1', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ], 
                                  "economics" : [ 
                                                 { "note" : "mynote1", "budget" : 3, "invoiced" : 0, "period" : "2005-10-08", "extra" : 1 },     
                                                 { "note" : "mynote2", "budget" : 5, "invoiced" : 0,  "period" : "2005-11-08", "extra" : 4 }, 
                                                 { "note" : "mynote3", "budget" : 20, "invoiced" : 0,  "period" : "2005-12-08", "extra" : 8 } ],
                                  'expences' : [ 
                                                 { '_id' : '6'*24, "user_id" : '1'*24, "trip_id" : '3'*24, 'status' : 0, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2005-10-04', 'amount' : 5}, { 'date' : '2000-01-05', 'amount' : 10}] },
                                                 # Following expence is not approved     
                                                 { '_id' : '5'*24, "user_id" : '1'*24, "trip_id" : '4'*24, 'status' : 2, "date" : "2010-10-09", "file" : {}, 'objects' : [{ 'date' : '2005-10-09', 'amount' : 5}, { 'date' : '2000-01-09', 'amount' : 10}] }     
                                 ]
                                   
                                   },
                                 { 'customer' : 'CUSTOMER1', 'tags' : [ 'TYPE2' ], 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag2', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[0], 'name' : 'Emp2'} ], 
                                  'expences' : [ 
                                                 { '_id' : '7'*24, "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 0, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2003-04-10', 'amount' : 15}, { 'date' : '2005-01-05', 'amount' : 20}] },     
                                                 { '_id' : '8'*24, "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 0, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2009-01-04', 'amount' : 7}] }     
                                 ] 
                                   }, 
                                 { 'customer' : 'CUSTOMER3', 'tags' : [ 'TYPE3' ], 'name' : 'PROJECTNAME3', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : '1'*24, 'name' : 'Manag3', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[2], 'name' : 'Emp3'} ] } 
                                 ], 
                { 'error' : None, 'ids' : [ '', '', '' ] }
                )
        self.projects_ids = projects_json['ids']

        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }, { '_id' : self.projects_ids[1] }, { '_id' : self.projects_ids[2] }  ], { 'error' : None }))
 
        # Insert the day 17 for the first user                                   
        self._assert_req('/data/push_days', [ {'date': '2005-10-17', 
                                      'users': [ 
                                                { 'user_id' : self.users_ids[0], 
                                                 'hours': [
                                                           {u'note': u'FIRST 4 HOURS', u'task': 0, u'isextra': False, u'project': self.projects_ids[0], u'amount': 4}, 
                                                           {u'note': u'SECOND 4 HOURS', u'task': 0, u'isextra': False, u'project': self.projects_ids[1], u'amount': 4}
                                                           ]
                                                 }
                                                ]
                                      }
                                    ], { 'error' : None })   
        # Push in another day for second user                                      
        self._assert_req('/data/push_days', [ {'date': '2009-10-17', 
                                      'users': [ 
                                                { 'user_id' : self.users_ids[1], 
                                                 'hours': []
                                                 }
                                                ]
                                      }
                                    ], { 'error' : None })  
        
        # Push for the last day also third user
        self._assert_req('/data/push_days', [ {'date': '2009-10-17', 
                                      'users': [ 
                                                { 'user_id' : self.users_ids[2], 
                                                 'hours': [
                                                           {u'note': u'8 HOURS', u'task': 0, u'isextra': True, u'project': self.projects_ids[0], u'amount': 8}, 
                                                           ]
                                                 }
                                                ]
                                      }
                                    ], { 'error' : None })  
        
        
        
        # Delete all inserted days
        self.execOnTearDown.append(('/remove/day', [ { "date" :  "2005-10-17" },  { "date" :  "2009-10-17" } ] , { 'error' : None }))
        

  
class ReportProjectsAPIAsAdmin(TestClassBase, ModuleData):
      
  
    def setUp(self):        
        TestClassBase.setUp(self)
        ModuleData._add_module_data(self, '1'*24)
      
    def test_report_project_ok(self):
          
        self.maxDiff = None
        
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [],
                                                      'customers' : []
                                      }
                                    , {u'records': [[u'2000-01', { 'costs' : 10, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2003-04', { 'costs' : 15, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2005-01', { 'costs' : 20, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2005-10', { 'costs' : 5, u'salary': 40.0, u'budget': 3, u'extra_budget': 1}], [u'2005-11', { 'costs' : 0, u'salary': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', { 'costs' : 0, u'salary': 0, u'budget': 20, u'extra_budget': 8}], [u'2009-01', { 'costs' : 7, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2009-10', { 'costs' : 0, u'salary': 920.0, u'budget': 0, u'extra_budget': 0}]], u'error': None}
                                    )
        
        # Restrict time span             
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2006-02-02',
                                                      'projects' : [],
                                                      'customers' : []
                                      }
                                    , {u'records': [[u'2000-01', { 'costs' : 10, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2003-04', { 'costs' : 15, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2005-01', { 'costs' : 20, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2005-10', { 'costs' : 5, u'salary': 40.0, u'budget': 3, u'extra_budget': 1}], [u'2005-11', { 'costs' : 0, u'salary': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', { 'costs' : 0, u'salary': 0, u'budget': 20, u'extra_budget': 8}]], u'error': None}
                                    )

        # Restrict projects
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[0] ],
                                                      'customers' : []
                                      }
                                    , {u'records': [[u'2000-01', { 'costs' : 10, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2005-10', { 'costs' : 5, u'salary': 20.0, u'budget': 3, u'extra_budget': 1}], [u'2005-11', { 'costs' : 0, u'salary': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', { 'costs' : 0, u'salary': 0, u'budget': 20, u'extra_budget': 8}], [u'2009-10', { 'costs' : 0, u'salary': 920.0, u'budget': 0, u'extra_budget': 0}]], u'error': None}
                                    )


        # Search by type
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [],
                                                      'customers' : [],
                                                      'tags' : [ 'TYPE1' ]
                                      }
                                    , {u'records': [[u'2000-01', {u'salary': 0, u'costs': 10, u'budget': 0, u'extra_budget': 0}], [u'2005-10', {u'salary': 20.0, u'costs': 5, u'budget': 3, u'extra_budget': 1}], [u'2005-11', {u'salary': 0, u'costs': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', {u'salary': 0, u'costs': 0, u'budget': 20, u'extra_budget': 8}], [u'2009-10', {u'salary': 920.0, u'costs': 0, u'budget': 0, u'extra_budget': 0}]], u'error': None}
                                    )

        # Search by types
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [],
                                                      'customers' : [],
                                                      'tags' : [ 'TYPE1', 'TYPE2', 'TYPE3' ]
                                      }
                                    , {u'records': [[u'2000-01', {u'salary': 0, u'costs': 10, u'budget': 0, u'extra_budget': 0}], [u'2003-04', {u'salary': 0, u'costs': 15, u'budget': 0, u'extra_budget': 0}], [u'2005-01', {u'salary': 0, u'costs': 20, u'budget': 0, u'extra_budget': 0}], [u'2005-10', {u'salary': 40.0, u'costs': 5, u'budget': 3, u'extra_budget': 1}], [u'2005-11', {u'salary': 0, u'costs': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', {u'salary': 0, u'costs': 0, u'budget': 20, u'extra_budget': 8}], [u'2009-01', {u'salary': 0, u'costs': 7, u'budget': 0, u'extra_budget': 0}], [u'2009-10', {u'salary': 920.0, u'costs': 0, u'budget': 0, u'extra_budget': 0}]], u'error': None}
                                    )
        
        # Search using multiple factors
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[2] ],
                                                      'customers' : [ 'CUSTOMER1' ],
                                                      'tags' : [ 'TYPE1' ]
                                      }
                                    , {u'records': [[u'2000-01', {u'salary': 0, u'costs': 10, u'budget': 0, u'extra_budget': 0}], [u'2003-04', {u'salary': 0, u'costs': 15, u'budget': 0, u'extra_budget': 0}], [u'2005-01', {u'salary': 0, u'costs': 20, u'budget': 0, u'extra_budget': 0}], [u'2005-10', {u'salary': 40.0, u'costs': 5, u'budget': 3, u'extra_budget': 1}], [u'2005-11', {u'salary': 0, u'costs': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', {u'salary': 0, u'costs': 0, u'budget': 20, u'extra_budget': 8}], [u'2009-01', {u'salary': 0, u'costs': 7, u'budget': 0, u'extra_budget': 0}], [u'2009-10', {u'salary': 920.0, u'costs': 0, u'budget': 0, u'extra_budget': 0}]], u'error': None}
                                    )
        
        

    def test_report_project_modeproject_ok(self):
          
        self.maxDiff = None
        
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [],
                                                      'customers' : [],
                                                      'mode' : 'project'
                                      }
                                    , {u'records': { self.projects_ids[1]: [[u'2003-04', {u'salary': 0, u'costs': 15, u'budget': 0, u'extra_budget': 0}], [u'2005-01', {u'salary': 0, u'costs': 20, u'budget': 0, u'extra_budget': 0}], [u'2005-10', {u'salary': 20.0, u'costs': 0, u'budget': 0, u'extra_budget': 0}], [u'2009-01', {u'salary': 0, u'costs': 7, u'budget': 0, u'extra_budget': 0}]], self.projects_ids[0]: [[u'2000-01', { 'costs' : 10, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2005-10', { 'costs' : 5, u'salary': 20.0, u'budget': 3, u'extra_budget': 1}], [u'2005-11', { 'costs' : 0, u'salary': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', { 'costs' : 0, u'salary': 0, u'budget': 20, u'extra_budget': 8}], [u'2009-10', { 'costs' : 0, u'salary': 920.0, u'budget': 0, u'extra_budget': 0}]]}, u'error': None}
                                    )
        
        # Restrict time span             
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2006-02-02',
                                                      'projects' : [],
                                                      'customers' : [],
                                                      'mode' : 'project'
                                      }
                                    , {u'error': None,  u'records': { self.projects_ids[0] : [[u'2000-01', {u'salary': 0, u'costs': 10, u'budget': 0, u'extra_budget': 0}], [u'2005-10', {u'salary': 20.0, u'costs': 5, u'budget': 3, u'extra_budget': 1}], [u'2005-11', {u'salary': 0, u'costs': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', {u'salary': 0, u'costs': 0, u'budget': 20, u'extra_budget': 8}]], self.projects_ids[1]: [[u'2003-04', {u'salary': 0, u'costs': 15, u'budget': 0, u'extra_budget': 0}], [u'2005-01', {u'salary': 0, u'costs': 20, u'budget': 0, u'extra_budget': 0}], [u'2005-10', {u'salary': 20.0, u'costs': 0, u'budget': 0, u'extra_budget': 0}]]}}
                                    )

        # Restrict projects
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[0] ],
                                                      'customers' : [],
                                                      'mode' : 'project'
                                      }
                                    , {u'error': None, u'records': { self.projects_ids[0]: [[u'2000-01', { 'costs' : 10, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2005-10', { 'costs' : 5, u'salary': 20.0, u'budget': 3, u'extra_budget': 1}], [u'2005-11', { 'costs' : 0, u'salary': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', { 'costs' : 0, u'salary': 0, u'budget': 20, u'extra_budget': 8}], [u'2009-10', { 'costs' : 0, u'salary': 920.0, u'budget': 0, u'extra_budget': 0}]] } }
                                    )






class ReportUsersHoursAPIAsManager(TestCaseAsManager, ModuleData):
    
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.manager_id)
        self._log_as_user()
 
    def test_report_project_ok(self):
  
        # Search by project
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[0] ],
                                                      'customers' : []
                                      }
                                    , {u'records': [[u'2000-01', { 'costs' : 10, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2005-10', { 'costs' : 5, u'salary': 20.0, u'budget': 3, u'extra_budget': 1}], [u'2005-11', { 'costs' : 0, u'salary': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', { 'costs' : 0, u'salary': 0, u'budget': 20, u'extra_budget': 8}], [u'2009-10', { 'costs' : 0, u'salary': 920.0, u'budget': 0, u'extra_budget': 0}]], u'error': None}
                                    )

        # Search by customer
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [  ],
                                                      'customers' : [ 'CUSTOMER' ]
                                      }
                                    , {u'records': [[u'2000-01', { 'costs' : 10, u'salary': 0, u'budget': 0, u'extra_budget': 0}], [u'2005-10', { 'costs' : 5, u'salary': 20.0, u'budget': 3, u'extra_budget': 1}], [u'2005-11', { 'costs' : 0, u'salary': 0, u'budget': 5, u'extra_budget': 4}], [u'2005-12', { 'costs' : 0, u'salary': 0, u'budget': 20, u'extra_budget': 8}], [u'2009-10', { 'costs' : 0, u'salary': 920.0, u'budget': 0, u'extra_budget': 0}]], u'error': None}
                                    )
         
    def test_report_project_ko(self):

        # Search without specify project
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-03-03', 
                                                      'end' : '2020-03-03',
                                                      'projects' : [  ],
                                                      'customers' : []
                                      }
                                    , {u'error': "ValidationError: 'users.hours.project' is a required property" }
                                    )
        
        # Search with wrong project
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[2] ],
                                                      'customers' : []
                                      }
                                    , {u'error': "ValidationError: u'%s' is not one of ['%s', '%s']" % (self.projects_ids[2], self.projects_ids[0], self.projects_ids[1])}
                                    )
        
        # Search with wrong customer
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [  ],
                                                      'customers' : [ 'CUSTOMER2' ]
                                      }
                                    , {u'error': "ValidationError: 'users.hours.project' is a required property" }
                                    )


class ReportUsersHoursAPIAsUser(TestCaseAsEmployee, ModuleData):
    
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.employee_id)
        self._log_as_user()
        
    def test_report_project_ko(self):
          
        self.maxDiff = None
          
        # Search by project
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[0] ],
                                                      'customers' : []
                                      }
                                    , {u'error': "TSValidationError: Access to 'report_projects' is restricted for current user"}
                                    )  