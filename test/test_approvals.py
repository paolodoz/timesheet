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
                                  'expences' : [ 
                                                 { '_id' : '6'*24, "user_id" : '1'*24, "trip_id" : '3'*24, 'status' : 1, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2005-10-04', 'amount' : 5}, { 'date' : '2000-01-05', 'amount' : 10}] },
                                                 { '_id' : '5'*24, "user_id" : '1'*24, "trip_id" : '4'*24, 'status' : 2, "date" : "2010-10-09", "file" : {}, 'objects' : [{ 'date' : '2005-10-09', 'amount' : 5}, { 'date' : '2000-01-09', 'amount' : 10}] }     
                                 ]
                                   
                                   },
                                 { 'customer' : 'CUSTOMER1', 'tags' : [ 'TYPE2' ], 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsible' : { '_id' : current_id, 'name' : 'Manag2'}, 'employees' : [ { '_id' : self.users_ids[0], 'name' : 'Emp2'} ], 
                                  'expences' : [ 
                                                 { '_id' : '7'*24, "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 1, "date" : "2010-10-07", "file" : {}, 'objects' : [{ 'date' : '2003-04-10', 'amount' : 15}, { 'date' : '2005-01-05', 'amount' : 20}] },     
                                                 { '_id' : '8'*24, "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 0, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2009-01-04', 'amount' : 7}] }     
                                 ] 
                                   }, 
                                 { 'customer' : 'CUSTOMER3', 'tags' : [ 'TYPE3' ], 'name' : 'PROJECTNAME3', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsible' : { '_id' : '1'*24, 'name' : 'Manag3'}, 'employees' : [ { '_id' : self.users_ids[2], 'name' : 'Emp3'} ],
                                  'trips' : [ 
                                                 { '_id' : '8'*24, "user_id" : '1'*24, "description" : "trip1", "status" : 0, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },     
                                                 { '_id' : '9'*24, "user_id" : current_id, "description" : "trip2", "status" : 1, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },    
                                                 { '_id' : '3'*24, "user_id" : current_id, "description" : "trip3", "status" : -1, "start" : "2010-10-10", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} }     
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

    def test_approve_ok(self):

        # Decrement status flow of '6'*24
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '6'*24, 'action' : 'approve', 'note' : 'asd'  }, 
               { 'error' : None, 'status' : 0 }
           )
         
        # Decrement again (should remain 0) of '6'*24
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '6'*24, 'action' : 'approve', 'note' : 'asd2'  }, 
               { 'error' : None, 'status' : 0 }
           )
    
        # Reject '5'*24
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '5'*24, 'action' : 'reject', 'note' : 'asd3'  }, 
               { 'error' : None, 'status' : -2 }
           )
  
        # Search all approvals with project_id
        self._assert_req('/data/search_approvals',  { 'project_id' : self.projects_ids[0], 'status' : 'any' }, 
               {u'error': None,
                 u'expences': [{u'_id': '',
                                u'date': u'2010-10-08',
                                u'file': {},
                                u'notes': [u'asd', u'asd2'],
                                u'objects': [{u'amount': 5, u'date': u'2005-10-04'},
                                             {u'amount': 10, u'date': u'2000-01-05'}],
                                u'project_id': self.projects_ids[0],
                                u'status': 0,
                                u'trip_id': u'333333333333333333333333',
                                u'user_id': u'111111111111111111111111'},
                               {u'_id': '',
                                u'date': u'2010-10-09',
                                u'file': {},
                                u'notes': [u'asd3'],
                                u'objects': [{u'amount': 5, u'date': u'2005-10-09'},
                                             {u'amount': 10, u'date': u'2000-01-09'}],
                                u'project_id': self.projects_ids[0],
                                u'status': -2,
                                u'trip_id': u'444444444444444444444444',
                                u'user_id': u'111111111111111111111111'}],
                 u'trips': []}
           )
  
    def test_approval_search_ok(self):
  
        # Search all with pendance approvation
        self._assert_req('/data/search_approvals',  {  }, 
               {'error': None, 'expences': [
                        {'_id': '',
                           'date': '2010-10-07',
                           'file': {},
                           'objects': [{'amount': 15,
                                        'date': '2003-04-10'},
                                       {'amount': 20,
                                        'date': '2005-01-05'}],
                           'project_id': self.projects_ids[1],
                           'status': 1,
                           'trip_id': '222222222222222222222222',
                           'user_id': '111111111111111111111111'},
                          {'_id': '',
                           'date': '2010-10-08',
                           'file': {},
                           'objects': [{'amount': 5, 'date': '2005-10-04'},
                                       {'amount': 10,
                                        'date': '2000-01-05'}],
                           'project_id': self.projects_ids[0],
                           'status': 1,
                           'trip_id': '333333333333333333333333',
                           'user_id': '111111111111111111111111'},
                          {'_id': '',
                           'date': '2010-10-09',
                           'file': {},
                           'objects': [{'amount': 5, 'date': '2005-10-09'},
                                       {'amount': 10,
                                        'date': '2000-01-09'}],
                           'project_id': self.projects_ids[0],
                           'status': 2,
                           'trip_id': '444444444444444444444444',
                           'user_id': '111111111111111111111111'},
                                            ],
             'trips': [
                       {'_id': '',
                        'accommodation': {},
                        'city': 'Rome',
                        'country': 'Italy',
                        'description': 'trip2',
                        'end': '2010-10-10',
                        'notes': ['approved'],
                        'project_id': self.projects_ids[2],
                        'start': '2010-10-08',
                        'status': 1,
                        'user_id': '111111111111111111111111'},]}
           )
  
   
  
 
        # Search the ones to approve with project_id
        self._assert_req('/data/search_approvals',  { 'project_id' : self.projects_ids[2] }, 
               {'error': None,  
             'expences' : [],
             'trips': [
                       {'_id': '',
                        'accommodation': {},
                        'city': 'Rome',
                        'country': 'Italy',
                        'description': 'trip2',
                        'end': '2010-10-10',
                        'notes': ['approved'],
                        'project_id': self.projects_ids[2],
                        'start': '2010-10-08',
                        'status': 1,
                        'user_id': '111111111111111111111111'}
                       ]}
           )
          
   
   
        # Search any expences
        self._assert_req('/data/search_approvals',  { 'type' : 'expences', 'status' : 'any' }, 
               {'error': None, 'expences': [
                        {'_id': '',
                           'date': '2010-10-07',
                           'file': {},
                           'objects': [{'amount': 15,
                                        'date': '2003-04-10'},
                                       {'amount': 20,
                                        'date': '2005-01-05'}],
                           'project_id': self.projects_ids[1],
                           'status': 1,
                           'trip_id': '222222222222222222222222',
                           'user_id': '111111111111111111111111'},
                          {
                           '_id': '',
                           'date': '2010-10-08',
                           'file': {},
                           'objects': [{'amount': 7, 'date': '2009-01-04'}],
                           'project_id': self.projects_ids[1],
                           'status': 0,
                           'trip_id': '222222222222222222222222',
                           'user_id': '111111111111111111111111'},
                          {'_id': '',
                           'date': '2010-10-08',
                           'file': {},
                           'objects': [{'amount': 5, 'date': '2005-10-04'},
                                       {'amount': 10,
                                        'date': '2000-01-05'}],
                           'project_id': self.projects_ids[0],
                           'status': 1,
                           'trip_id': '333333333333333333333333',
                           'user_id': '111111111111111111111111'},
                          {'_id': '',
                           'date': '2010-10-09',
                           'file': {},
                           'objects': [{'amount': 5, 'date': '2005-10-09'},
                                       {'amount': 10,
                                        'date': '2000-01-09'}],
                           'project_id': self.projects_ids[0],
                           'status': 2,
                           'trip_id': '444444444444444444444444',
                           'user_id': '111111111111111111111111'},
                                            ], 'trips' : []
                },
           )
    
        # Search both trips approved and rejected 
        self._assert_req('/data/search_approvals',  {  'type' : 'trips', 'status' : 'any' }, 
               {'error': None,  
             'expences' : [],
             'trips': [
                       {'_id': '',
                        'accommodation': {},
                        'city': 'Rome',
                        'country': 'Italy',
                        'description': 'trip2',
                        'end': '2010-10-10',
                        'notes': ['approved'],
                        'project_id': self.projects_ids[2],
                        'start': '2010-10-08',
                        'status': 1,
                        'user_id': '111111111111111111111111'},
                       {'_id': '',
                        'accommodation': {},
                        'city': 'Rome',
                        'country': 'Italy',
                        'description': 'trip1',
                        'end': '2010-10-10',
                        'notes': ['approved'],
                        'project_id': self.projects_ids[2],
                        'start': '2010-10-08',
                        'status': 0,
                        'user_id': '111111111111111111111111'},
                        { '_id' : '', 
                         "user_id" : '1'*24, 
                         "description" : "trip3", 
                         "status" : -1, 
                         "start" : "2010-10-10", 
                         "end" : "2010-10-10", 
                         "country" : "Italy", 
                         'city' : "Rome", 
                         'notes' : [ 'approved' ], 
                         'accommodation' : {},
                         'project_id': self.projects_ids[2] }     
  
                       ]}
           ) 

       
        # Search only rejected 
        self._assert_req('/data/search_approvals',  {  'status' : 'rejected' }, 
               {'error': None,  
             'expences' : [],
             'trips': [
                        { '_id' : '', 
                         "user_id" : '1'*24, 
                         "description" : "trip3", 
                         "status" : -1, 
                         "start" : "2010-10-10", 
                         "end" : "2010-10-10", 
                         "country" : "Italy", 
                         'city' : "Rome", 
                         'notes' : [ 'approved' ], 
                         'accommodation' : {},
                         'project_id': self.projects_ids[2] }     
  
                       ]}
           )         
        
           
    def test_approve_ko(self):
            
        # Insert one expence
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'action' : 'approve', 'note' : 'asd'  }, 
               { 'error' : "ValidationError: {u'action': u'approve', u'note': u'asd', u'project_id': u'%s'} is not valid under any of the given schemas" % self.projects_ids[0]}
           )
  

class ApprovalAPIAsManager(TestCaseAsManager, ModuleData):
     
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.manager_id)
        self._log_as_user()
  
 
 
class ApprovalAPIAsUser(TestCaseAsEmployee, ModuleData):
     
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.employee_id)
        self._log_as_user()
