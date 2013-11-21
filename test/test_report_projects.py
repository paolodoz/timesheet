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
                                 { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE1' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsible' : { '_id' : current_id, 'name' : 'Manag1'}, 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ], 
                                  "economics" : [ 
                                                 { "note" : "mynote1", "budget" : 3, "invoiced" : 0, "period" : "2005-10-08", "extra" : 1 },     
                                                 { "note" : "mynote2", "budget" : 5, "invoiced" : 0,  "period" : "2005-11-08", "extra" : 4 }, 
                                                 { "note" : "mynote3", "budget" : 20, "invoiced" : 0,  "period" : "2005-12-08", "extra" : 8 } ] },
                                 { 'customer' : 'CUSTOMER1', 'tags' : [ 'TYPE2' ], 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsible' : { '_id' : current_id, 'name' : 'Manag2'}, 'employees' : [ { '_id' : self.users_ids[0], 'name' : 'Emp2'} ] }, 
                                 { 'customer' : 'CUSTOMER3', 'tags' : [ 'TYPE3' ], 'name' : 'PROJECTNAME3', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsible' : { '_id' : '1'*24, 'name' : 'Manag3'}, 'employees' : [ { '_id' : self.users_ids[2], 'name' : 'Emp3'} ] } 
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
                                    , {u'error': None, u'records': [[u'2005-10', {u'budget': 0, u'cost': 5*8, u'extra': 0}], [u'2009-10', {u'budget': 0, u'cost': 100*8 + 100*8*0.15, u'extra': 0}]]}
                                    )
        
        # Restrict time span             
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2006-02-02',
                                                      'projects' : [],
                                                      'customers' : []
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', {u'budget': 0, u'cost': 5*8, u'extra': 0}]]}
                                    )

        # Restrict projects
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[0] ],
                                                      'customers' : []
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', {u'budget': 3, u'cost': 5*4, u'extra': 1}], [u'2009-10', {u'budget': 0, u'cost': 100*8 + 100*8*0.15, u'extra': 0}]]}
                                    )


        # Search by type
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [],
                                                      'customers' : [],
                                                      'tags' : [ 'TYPE1' ]
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', {u'budget': 3, u'cost': 5*4, u'extra': 1}], [u'2009-10', {u'budget': 0, u'cost': 100*8 + 100*8*0.15, u'extra': 0}]]}
                                    )

        # Search by types
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [],
                                                      'customers' : [],
                                                      'tags' : [ 'TYPE1', 'TYPE2', 'TYPE3' ]
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', {u'budget': 0, u'cost': 5*8, u'extra': 0}], [u'2009-10', {u'budget': 0, u'cost': 100*8 + 100*8*0.15, u'extra': 0}]]}
                                    )
        
        # Search using multiple factors
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[2] ],
                                                      'customers' : [ 'CUSTOMER1' ],
                                                      'tags' : [ 'TYPE1' ]
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', {u'budget': 0, u'cost': 5*8, u'extra': 0}], [u'2009-10', {u'budget': 0, u'cost': 100*8 + 100*8*0.15, u'extra': 0}]]}
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
                                    , {u'error': None, u'records': { self.projects_ids[0] : [[u'2005-10', {u'budget': 3, u'cost': 5*4, u'extra': 1}], [u'2009-10', {u'budget': 0, u'cost': 100*8 + 100*8*0.15, u'extra': 0}]], 
                                                                    self.projects_ids[1]: [[u'2005-10', {u'budget': 0, u'cost': 5*4, u'extra': 0}]]}}
                                    )
        
        # Restrict time span             
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2006-02-02',
                                                      'projects' : [],
                                                      'customers' : [],
                                                      'mode' : 'project'
                                      }
                                    , {u'error': None,  u'records': { self.projects_ids[0] : [[u'2005-10', {u'budget': 3, u'cost': 5*4, u'extra': 1}]], self.projects_ids[1]: [[u'2005-10', {u'budget': 0, u'cost': 5*4, u'extra': 0}]]}}
                                    )

        # Restrict projects
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[0] ],
                                                      'customers' : [],
                                                      'mode' : 'project'
                                      }
                                    , {u'error': None, u'records': { self.projects_ids[0] : [[u'2005-10', {u'budget': 3, u'cost': 5*4, u'extra': 1}], [u'2009-10', {u'budget': 0, u'cost': 100*8 + 100*8*0.15, u'extra': 0}]] } }
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
                                    , {u'error': None, u'records': [[u'2005-10', {u'budget': 3, u'cost': 20, u'extra': 1}], [u'2009-10', {u'budget': 0, u'cost': 800 + 800*0.15, u'extra': 0}]]}
                                    )

        # Search by customer
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [  ],
                                                      'customers' : [ 'CUSTOMER' ]
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', {u'budget': 3, u'cost': 20, u'extra': 1}], [u'2009-10', {u'budget': 0, u'cost': 800 + 800*0.15, u'extra': 0}]]}
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