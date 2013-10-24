from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager

class ReportUsersHoursClassBase(TestClassBase):

    def setUp(self):
        TestClassBase.setUp(self)
        
        # Add two elements USERTEST1 and USERTEST2
        users_json = self._assert_req('/add/user', [ 
                                                    { 'name' : 'USERTEST1', 'surname' : 'SURNAME', 'username' : 'USERNAME1' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : []  }, 
                                                    { 'name' : 'USERTEST2', 'surname' : 'SURNAME', 'username' : 'USERNAME2' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER2', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : []  }, 
                                                    { 'name' : 'USERTEST3', 'surname' : 'SURNAME', 'username' : 'USERNAME3' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER3', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : []  } 
                                                    ], { 'error' : None, 'ids' : [ '', '', '' ] })
        self.users_ids = users_json['ids']
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.users_ids[0]  }, { '_id' : self.users_ids[1]  }, { '_id' : self.users_ids[2] } ], { 'error' : None }))
        
        # Add one project
        projects_json = self._assert_req('/add/project', [ 
                                 { 'customer' : 'CUSTOMER', 'type' : 'TYPE', 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2001-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'expences' : 4, 'responsible' : { '_id' : self.users_ids[0], 'name' : 'Manag1'}, 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ] },
                                 { 'customer' : 'CUSTOMER1', 'type' : 'TYPE', 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2004-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'expences' : 4, 'responsible' : { '_id' : self.users_ids[1], 'name' : 'Manag2'}, 'employees' : [ { '_id' : self.users_ids[0], 'name' : 'Emp2'} ] } 
                                 ], 
                { 'error' : None, 'ids' : [ '', '' ] }
                )
        self.projects_ids = projects_json['ids']
        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }, { '_id' : self.projects_ids[0] } ], { 'error' : None }))
 
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
        
    


class ReportUsersHoursAPIAsManager(TestCaseAsManager):
    
    def setUp(self):
        
        TestClassBase.setUp(self)
        
        # Add two elements USERTEST1 and USERTEST2
        users_json = self._assert_req('/add/user', [ 
                                                    { 'name' : 'USERTEST1', 'surname' : 'SURNAME', 'username' : 'USERNAME1' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : []  }, 
                                                    { 'name' : 'USERTEST2', 'surname' : 'SURNAME', 'username' : 'USERNAME2' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER2', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : []  }, 
                                                    { 'name' : 'USERTEST3', 'surname' : 'SURNAME', 'username' : 'USERNAME3' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER3', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'myotherpassword', 'salt' : '', 'salary' : []  } 
                                                    ], { 'error' : None, 'ids' : [ '', '', '' ] })
        self.users_ids = users_json['ids']
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.users_ids[0]  }, { '_id' : self.users_ids[1]  }, { '_id' : self.users_ids[2] } ], { 'error' : None }))
        
        # Add one project
        projects_json = self._assert_req('/add/project', [ 
                                 { 'customer' : 'CUSTOMER', 'type' : 'TYPE', 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2001-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'expences' : 4, 'responsible' : { '_id' : self.users_ids[0], 'name' : 'Manag1'}, 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ] },
                                 { 'customer' : 'CUSTOMER1', 'type' : 'TYPE', 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2004-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'expences' : 4, 'responsible' : { '_id' : self.users_ids[1], 'name' : 'Manag2'}, 'employees' : [ { '_id' : self.users_ids[0], 'name' : 'Emp2'} ] } 
                                 ], 
                { 'error' : None, 'ids' : [ '', '' ] }
                )
        self.projects_ids = projects_json['ids']
        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }, { '_id' : self.projects_ids[0] } ], { 'error' : None }))
 
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
        
        TestCaseAsManager.setUp(self)
    
    
    
    def test_day_ko(self):
        # Search only one user
        self._assert_req('/data/report_users_hours', {
                                                      'start': '2000-01-01', 
                                                      'end' : '2020-02-02',
                                                      'users_ids' :  [ self.users_ids[0] ],
                                                      'projects' : [],
                                                      'hours_standard': False,
                                                      'hours_extra' : False,
                                                      'tasks' : []
                                      }
                                    , { 'error': "ValidationError: 'users.hours.project' is a required property"}
                                    )        
         
     
 
class ReportUsersHoursAPIAsAdmin(ReportUsersHoursClassBase):
     
     
    def test_day_ok(self):
         
        self.maxDiff = None
         
        # Search only one user
        self._assert_req('/data/report_users_hours', {
                                                      'start': '2000-01-01', 
                                                      'end' : '2020-02-02',
                                                      'users_ids' :  [ self.users_ids[0] ],
                                                      'projects' : [],
                                                      'hours_standard': False,
                                                      'hours_extra' : False,
                                                      'tasks' : []
                                      }
                                    , {u'records': [
                                                    {u'hours': [
                                                                {u'note': u'FIRST 4 HOURS', 
                                                                 u'project': self.projects_ids[0], 
                                                                 u'amount': 4, 
                                                                 u'task': 0, 
                                                                 u'isextra': False}, 
                                                                {u'note': u'SECOND 4 HOURS', 
                                                                 u'project': self.projects_ids[1], 
                                                                 u'amount': 4, 
                                                                 u'task': 0, 
                                                                 u'isextra': False}], 
                                                     u'_id': {u'date': u'2005-10-17', 
                                                              u'user_id': self.users_ids[0]
                                                              }
                                                     }], u'error': None}
                                    )
          
        # Search both users
        self._assert_req('/data/report_users_hours', {
                                                      'start': '2000-01-01', 
                                                      'end' : '2020-02-02',
                                                      'users_ids' :  self.users_ids,
                                                      'projects' : [],
                                                      'hours_standard': False,
                                                      'hours_extra' : False,
                                                      'tasks' : []
                                      }
                                    , {u'records': 
                                       [
                                        {u'hours': [
                                                    {u'note': u'FIRST 4 HOURS', 
                                                     u'project': self.projects_ids[0], 
                                                     u'amount': 4, 
                                                     u'task': 0, 
                                                     u'isextra': False}, 
                                                    {u'note': u'SECOND 4 HOURS', 
                                                     u'project': self.projects_ids[1], 
                                                     u'amount': 4, 
                                                     u'task': 0, 
                                                     u'isextra': False}
                                                    ], u'_id': {
                                                                u'date': u'2005-10-17', 
                                                                u'user_id': self.users_ids[0]}
                                         }, {u'hours': [
                                                        {u'note': u'8 HOURS', 
                                                         u'project': self.projects_ids[0], 
                                                         u'amount': 8, 
                                                         u'task': 0, 
                                                         u'isextra': True}
                                                        ], u'_id': {u'date': u'2009-10-17', 
                                                                    u'user_id': self.users_ids[2]
                                                                    }
                                             }], u'error': None}
                                       )
          
        # Search both users who have only hours_extra
        self._assert_req('/data/report_users_hours', {
                                                      'start': '2000-01-01', 
                                                      'end' : '2020-02-02',
                                                      'users_ids' :  self.users_ids,
                                                      'projects' : [],
                                                      'hours_standard': False,
                                                      'hours_extra' : True,
                                                      'tasks' : []
                                      }
                                    , {u'records': 
                                       [{u'hours': [
                                                        {u'note': u'8 HOURS', 
                                                         u'project': self.projects_ids[0], 
                                                         u'amount': 8, 
                                                         u'task': 0, 
                                                         u'isextra': True}
                                                        ], u'_id': {u'date': u'2009-10-17', 
                                                                    u'user_id': self.users_ids[2]
                                                                    }
                                             }], u'error': None}
                                       )
          
        # Search in a short range
        self._assert_req('/data/report_users_hours', {
                                                      'start': '2020-02-01', 
                                                      'end' : '2020-02-02',
                                                      'users_ids' :  self.users_ids,
                                                      'projects' : [],
                                                      'hours_standard': False,
                                                      'hours_extra' : True,
                                                      'tasks' : []
                                      }
                                    , {u'records': 
                                       [], u'error': None}
                                       )         
         
