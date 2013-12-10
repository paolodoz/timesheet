from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager, TestCaseAsAccount, admin_data
from core.config import notifications

def _debug_notification(recipients, notification_type):
    notifications_result = {}
    
    for recipient in recipients:
        notifications_result[recipient['email']] = notifications.get_template('%s.tpl' % notification_type).render(**recipient)
    
    return [ notifications_result ]


class ModuleData:

    def _add_module_data(self, current_id):
        
        self.users_data = [ 
                        { 'name' : 'USERTEST1', 'surname' : 'SURNAME', 'username' : 'USERNAME1' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'employee', 'password' : 'mypassword', 'salt' : '', 'salary' : [ { 'cost' : 5, 'from': '2004-01-02', 'to' : '2006-01-02' }]  }, 
                        { 'name' : 'MANAGERTEST1', 'surname' : 'SURNAME', 'username' : 'MANAGERNAME1' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'project manager', 'password' : 'mypassword', 'salt' : '', 'salary' : [ ]  }, 
                        { 'name' : 'ACCOUNTEST1', 'surname' : 'SURNAME', 'username' : 'ACCOUNTNAME1' , 'email' : 'EMAIL@DOMAIN.COM', 'phone' : '123456789', 'mobile' : 'USER1', 'city' : 'USERCITY', 'group' : 'account', 'password' : 'mypassword', 'salt' : '', 'salary' : [  ]  }, 
                        ]
        
        # Add an element for every step
        users_json = self._assert_req('/add/user', self.users_data, { 'error' : None, 'ids' : [ '', '', '' ] })
        self.users_ids = users_json['ids'] 
        self.execOnTearDown.append(('/remove/user', [ { '_id' : self.users_ids[0]  }, { '_id' : self.users_ids[1]  }, { '_id' : self.users_ids[2]  }], { 'error' : None }))
        
        # Add projects
        projects_json = self._assert_req('/add/project', [ 
                                 { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE1' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag1', 'role' : 'project manager'}, { '_id' : current_id, 'name' : 'Manag1', 'role' : 'account'} ], 'employees' : [ { '_id' : self.users_ids[0], 'name' : 'Emp1'} ], 
                                  'expences' : [ 
                                                 { '_id' : '6'*24, "user_id" : '1'*24, "trip_id" : '3'*24, 'status' : 2, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2005-10-04', 'amount' : 5}, { 'date' : '2000-01-05', 'amount' : 10}] },
                                                 { '_id' : '5'*24, "user_id" : '1'*24, "trip_id" : '4'*24, 'status' : 3, "date" : "2010-10-09", "file" : {}, 'objects' : [{ 'date' : '2005-10-09', 'amount' : 5}, { 'date' : '2000-01-09', 'amount' : 10}] }     
                                 ]
                                   
                                   },
                                 { 'customer' : 'CUSTOMER1', 'tags' : [ 'TYPE2' ], 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag2', 'role' : 'project manager'} ], 'employees' : [ { '_id' : current_id, 'name' : 'Emp2'} ], 
                                  'expences' : [ 
                                                 { '_id' : '7'*24, "user_id" : '1'*24, "trip_id" : '2'*24, 'status' : 1, "date" : "2010-10-07", "file" : {}, 'objects' : [{ 'date' : '2003-04-10', 'amount' : 15}, { 'date' : '2005-01-05', 'amount' : 20}] },     
                                                 { '_id' : '8'*24, "user_id" : current_id, "trip_id" : '2'*24, 'status' : 3, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2009-01-04', 'amount' : 7}] }     
                                 ] 
                                   }, 
                                 { 'customer' : 'CUSTOMER3', 'tags' : [ 'TYPE3' ], 'name' : 'PROJECTNAME3', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag3', 'role' : 'project manager'} ], 'employees' : [ { '_id' : current_id, 'name' : 'Emp3'} ],
                                  'trips' : [ 
                                                 { '_id' : '4'*24, "user_id" : '1'*24, "description" : "trip1", "status" : 2, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },     
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
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '6'*24, 'action' : 'approve', 'note' : 'ndee'  }, 
               { 'error' : None, 'status' : 1, 'notifications' : _debug_notification(self.admin_data, 'notify_new') }
           )
          
        # Decrement again '6'*24
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '6'*24, 'action' : 'approve', 'note' : 'ndee2'  }, 
               { 'error' : None, 'status' : 0, 'notifications' : _debug_notification(self.admin_data, 'notify_new') }
           )

        # Decrement again (should remain 0) '6'*24
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '6'*24, 'action' : 'approve', 'note' : 'asd2'  }, 
               { 'error' : None, 'status' : 0, 'notifications' : _debug_notification(self.admin_data, 'notify_new') }
           )
     
        # Reject '5'*24
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '5'*24, 'action' : 'reject', 'note' : 'asd3'  }, 
               { 'error' : None, 'status' : -3, 'notifications' : _debug_notification(self.admin_data, 'notify_reject') }
           )
   
        # Search all approvals with project_id
        self._assert_req('/data/search_approvals',  { 'projects_id' : [ self.projects_ids[0] ], 'status' : 'any' }, 
               {u'error': None,
                 u'expences': [{u'_id': '',
                                u'date': u'2010-10-08',
                                u'file': {},
                                u'notes': [ u'ndee', 'ndee2', u'asd2' ],
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
                                u'status': -3,
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
                          { '_id' : '', 
                           "user_id" : '1'*24, 
                           "trip_id" : '2'*24, 
                           'status' : 3, 
                           "date" : "2010-10-08", 
                           "file" : {}, 
                           'project_id': self.projects_ids[1],
                           'objects' : [{ 'date' : '2009-01-04', 'amount' : 7}] 
                           },
                          {'_id': '',
                           'date': '2010-10-08',
                           'file': {},
                           'objects': [{'amount': 5, 'date': '2005-10-04'},
                                       {'amount': 10,
                                        'date': '2000-01-05'}],
                           'project_id': self.projects_ids[0],
                           'status': 2,
                           'trip_id': '333333333333333333333333',
                           'user_id': '111111111111111111111111'},
                          {'_id': '',
                           'date': '2010-10-09',
                           'file': {},
                           'objects': [{'amount': 5, 'date': '2005-10-09'},
                                       {'amount': 10,
                                        'date': '2000-01-09'}],
                           'project_id': self.projects_ids[0],
                           'status': 3,
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
                        'user_id': '111111111111111111111111'},
                        
                        { '_id' : '', 
                         "user_id" : '1'*24, 
                         "description" : "trip1", 
                        'project_id': self.projects_ids[2],
                         "status" : 2, 
                         "start" : "2010-10-08", 
                         "end" : "2010-10-10", 
                         "country" : "Italy", 
                         'city' : "Rome", 
                         'notes' : [ 'approved' ], 
                         'accommodation' : {} },     
 
                       ]}
           )
   
    
        # Search the ones to approve with project_id
        self._assert_req('/data/search_approvals',  { 'projects_id' : [ self.projects_ids[2] ] }, 
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
                        { '_id' : '', 
                         "user_id" : '1'*24, 
                         "description" : "trip1", 
                        'project_id': self.projects_ids[2],
                         "status" : 2, 
                         "start" : "2010-10-08", 
                         "end" : "2010-10-10", 
                         "country" : "Italy", 
                         'city' : "Rome", 
                         'notes' : [ 'approved' ], 
                         'accommodation' : {} },     
                        
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
                           'status': 3,
                           'trip_id': '222222222222222222222222',
                           'user_id': '111111111111111111111111'},
                          {'_id': '',
                           'date': '2010-10-08',
                           'file': {},
                           'objects': [{'amount': 5, 'date': '2005-10-04'},
                                       {'amount': 10,
                                        'date': '2000-01-05'}],
                           'project_id': self.projects_ids[0],
                           'status': 2,
                           'trip_id': '333333333333333333333333',
                           'user_id': '111111111111111111111111'},
                          {'_id': '',
                           'date': '2010-10-09',
                           'file': {},
                           'objects': [{'amount': 5, 'date': '2005-10-09'},
                                       {'amount': 10,
                                        'date': '2000-01-09'}],
                           'project_id': self.projects_ids[0],
                           'status': 3,
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
                        'status': 2,
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
 
    def test_approve_ok(self):
 
        # Decrement status flow of '6'*24, that was 2 (correct flow)
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '6'*24, 'action' : 'approve', 'note' : 'asd'  }, 
               { 'error' : None, 'status' : 1, 'notifications' : _debug_notification(self.manager_data, 'notify_new') }
           )
          
        # Try to decrement again '6'*24, but is not reachable anymore
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '6'*24, 'action' : 'approve', 'note' : 'asd2'  }, 
               {u'error': u"TSValidationError: Can't find selected expence"}
           )
     
        # Try to reject '5'*24, is rejectable although on draft
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '5'*24, 'action' : 'reject', 'note' : 'asd3'  }, 
               { 'error' : None, 'status' : -3, 'notifications' : _debug_notification(admin_data, 'notify_reject') }
           )
 
        # Search all approvals with project_id
        self._assert_req('/data/search_approvals',  { 'projects_id' : [ self.projects_ids[0] ], 'status' : 'any' }, 
               {u'error': None,
                 u'expences': [{u'_id': '',
                 u'date': u'2010-10-09',
                 u'file': {},
                 u'notes': [u'asd3'],
                 u'objects': [{u'amount': 5, u'date': u'2005-10-09'},
                              {u'amount': 10, u'date': u'2000-01-09'}],
                 u'project_id': self.projects_ids[0],
                 u'status': -3,
                 u'trip_id': u'444444444444444444444444',
                 u'user_id': u'111111111111111111111111'}],
                 u'trips': []}
           )
   
 
 
    def test_approval_search_ok(self):
    
        # Search all with pendance approvation
        self._assert_req('/data/search_approvals',  { 'projects_id' : self.projects_ids }, 
               {'error': None, 'expences': [
                          {'_id': '',
                           'date': '2010-10-08',
                           'file': {},
                           'objects': [{'amount': 5, 'date': '2005-10-04'},
                                       {'amount': 10,
                                        'date': '2000-01-05'}],
                           'project_id': self.projects_ids[0],
                           'status': 2,
                           'trip_id': '333333333333333333333333',
                           'user_id': '111111111111111111111111'}],
             'trips': [                        
                       { '_id' : '', 
                         "user_id" : '1'*24, 
                         "description" : "trip1", 
                        'project_id': self.projects_ids[2],
                         "status" : 2, 
                         "start" : "2010-10-08", 
                         "end" : "2010-10-10", 
                         "country" : "Italy", 
                         'city' : "Rome", 
                         'notes' : [ 'approved' ], 
                         'accommodation' : {} }]}
           )
    
 
        # Search the ones to approve with project_id
        self._assert_req('/data/search_approvals',  { 'projects_id' : [ self.projects_ids[2] ] }, 
               {'error': None,  
             'expences' : [],
             'trips': [
                       { '_id' : '', 
                         "user_id" : '1'*24, 
                         "description" : "trip1", 
                        'project_id': self.projects_ids[2],
                         "status" : 2, 
                         "start" : "2010-10-08", 
                         "end" : "2010-10-10", 
                         "country" : "Italy", 
                         'city' : "Rome", 
                         'notes' : [ 'approved' ], 
                         'accommodation' : {} }
                       ]}
           )
     
        # Search any expences
        self._assert_req('/data/search_approvals',  { 'projects_id' : self.projects_ids, 
                                                     'type' : 'expences', 'status' : 'any' }, 
               {'error': None, 'expences': [
                        {'_id': '',
                           'date': '2010-10-08',
                           'file': {},
                           'objects': [{'amount': 5, 'date': '2005-10-04'},
                                       {'amount': 10,
                                        'date': '2000-01-05'}],
                           'project_id': self.projects_ids[0],
                           'status': 2,
                           'trip_id': '333333333333333333333333',
                           'user_id': '111111111111111111111111'},
                                            ], 'trips' : []
                },
           )
      
        # Search all trips
        self._assert_req('/data/search_approvals',  {  'type' : 'trips', 'status' : 'any', 'projects_id' : self.projects_ids }, 
               {'error': None,  
             'expences' : [],
             'trips': [
                       { '_id' : '', 
                         "user_id" : '1'*24, 
                         "description" : "trip1", 
                        'project_id': self.projects_ids[2],
                         "status" : 2, 
                         "start" : "2010-10-08", 
                         "end" : "2010-10-10", 
                         "country" : "Italy", 
                         'city' : "Rome", 
                         'notes' : [ 'approved' ], 
                         'accommodation' : {} },
                       
                       { '_id' : '', 
                         "user_id" : self.manager_id, 
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
        self._assert_req('/data/search_approvals',  {  'status' : 'rejected', 'projects_id' : self.projects_ids }, 
               {'error': None,  
             'expences' : [],
             'trips': [
                        { '_id' : '', 
                         "user_id" : self.manager_id, 
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
  
  
class ApprovalAPIAsUser(TestCaseAsEmployee, ModuleData):
      
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.employee_id)
        self._log_as_user()
 
    def test_approve_ok(self):
 
        # For the employees, user_id and project_id are required
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '6'*24, 'action' : 'approve', 'note' : 'asd'  }, 
               {u'error': u"ValidationError: 'user_id' is a required property"}
           )
 
        # Search project with no permissions
        self._assert_req('/data/approval',  { 'user_id' : self.employee_id, 'project_id' : self.projects_ids[0], 'expence_id' : '6'*24, 'action' : 'approve', 'note' : 'asd'  }, 
               {u'error': u"ValidationError: u'%s' is not one of %s" % (self.projects_ids[0], [ str(p) for p in self.projects_ids[1:] ])}
           )
          
        # Decrement '8'*24
        self._assert_req('/data/approval',  { 'user_id' : self.employee_id, 'project_id' : self.projects_ids[1], 'expence_id' : '8'*24, 'action' : 'approve', 'note' : 'asd2'  }, 
               { 'error' : None, 'status' : 2, 'notifications' : _debug_notification(self.employee_data, 'notify_new') }
           )
       
        # Try to reject '8'*24, but is not = 2 anymore
        self._assert_req('/data/approval',  {  'user_id' : self.employee_id, 'project_id' : self.projects_ids[1], 'expence_id' : '5'*24, 'action' : 'reject', 'note' : 'asd3'  }, 
               {u'error': u"TSValidationError: Can't find selected expence" }
           )
  
    def test_reject_ok(self):
 
        # Reject '8'*24 = 3 
        self._assert_req('/data/approval',  { 'user_id' : self.employee_id, 'project_id' : self.projects_ids[1], 'expence_id' : '8'*24, 'action' : 'reject', 'note' : 'asd2'  }, 
               { 'error' : None, 'status' : -3, 'notifications' : _debug_notification(self.employee_data, 'notify_reject') }
           )
    
        # Search all approvals
        self._assert_req('/data/search_approvals',  { 'projects_id' : [ self.projects_ids[1] ],  'user_id' : self.employee_id, 'status' : 'any' }, 
               {u'error': None,
                 u'expences': [{
                           '_id': '',
                           'date': '2010-10-08',
                           'file': {},
                           'objects': [{'amount': 7, 'date': '2009-01-04'}],
                           'project_id': self.projects_ids[1],
                           'status': -3,
                           'notes' : [ 'asd2' ],
                           'trip_id': '222222222222222222222222',
                           'user_id': self.employee_id},
                               ],
                 u'trips': []}
           )
   
  
    def test_approval_search_ok(self):
      
        # Search all with pendance approvation
        self._assert_req('/data/search_approvals',  { 'projects_id' : self.projects_ids[1:],  'user_id' : self.employee_id }, 
               {'error': None, 
                'expences': [
                       { '_id' : '', 
                        "user_id" : self.employee_id, 
                        "trip_id" : '2'*24, 
                        'project_id': self.projects_ids[1],
                        'status' : 3, 
                        "date" : "2010-10-08", 
                        "file" : {}, 
                        'objects' : [{ 'date' : '2009-01-04', 'amount' : 7}] }     
                             ],
             'trips': [ ]}
           )
     
  
        # Search the ones to approve with project_id
        self._assert_req('/data/search_approvals',  { 'projects_id' : [ self.projects_ids[1] ], 'user_id' : self.employee_id  }, 
               {'error': None,  
             'expences' : [
                            
                       { '_id' : '', 
                        "user_id" : self.employee_id, 
                        "trip_id" : '2'*24, 
                        'project_id': self.projects_ids[1],
                        'status' : 3, 
                        "date" : "2010-10-08", 
                        "file" : {}, 
                        'objects' : [{ 'date' : '2009-01-04', 'amount' : 7}] }     
                              
                           ],
             'trips': [ ]}
           )
      
        # Search any expences
        self._assert_req('/data/search_approvals',  { 'user_id' : self.employee_id, 'projects_id' : [ self.projects_ids[1], self.projects_ids[2] ], 'type' : 'expences', 'status' : 'any' }, 
               {'error': None, 'expences': [
                            
                       { '_id' : '', 
                        "user_id" : self.employee_id, 
                        "trip_id" : '2'*24, 
                        'project_id': self.projects_ids[1],
                        'status' : 3, 
                        "date" : "2010-10-08", 
                        "file" : {}, 
                        'objects' : [{ 'date' : '2009-01-04', 'amount' : 7}] }     
                              
                           ], 'trips' : []
                },
           )
 
 
       
        # search only rejected 
        self._assert_req('/data/search_approvals',  { 'user_id' : self.employee_id, 'projects_id' : [ self.projects_ids[1], self.projects_ids[2] ], 'status' : 'rejected' }, 
               {'error': None,  
             'expences' : [],
             'trips': [
                    { '_id' : '', 
                     "user_id" : self.employee_id, 
                     'project_id' : self.projects_ids[2],
                     "description" : "trip3", 
                     "status" : -1, 
                     "start" : "2010-10-10", 
                     "end" : "2010-10-10", 
                     "country" : "Italy", 
                     'city' : "Rome", 
                     'notes' : [ 'approved' ], 
                     'accommodation' : {} }     
                    ]}
           )         
           
              



class ApprovalAPIAsAccount(TestCaseAsAccount, ModuleData):
       
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.account_id)
        self._log_as_user()
  
    def test_approve_ok(self):
  
        # Decrement status flow of '9'*24, that was 1 (correct flow)
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[2], 'trip_id' : '9'*24, 'action' : 'approve', 'note' : 'asd'  }, 
               { 'error' : None, 'status' : 0, 'notifications' : _debug_notification(self.account_data, 'notify_new') }
           )
          
        # Try to decrement again '4'*24, but is not reachable anymore
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[2], 'trip_id' : '9'*24, 'action' : 'approve', 'note' : 'asd'  }, 
               {u'error': u"TSValidationError: Can't find selected expence"}
           )
     
        # Try to reject '5'*24, is rejectable although on draft
        self._assert_req('/data/approval',  { 'project_id' : self.projects_ids[0], 'expence_id' : '5'*24, 'action' : 'reject', 'note' : 'asd3'  }, 
               { 'error' : None, 'status' : -3, 'notifications' : _debug_notification(admin_data, 'notify_reject') }
           )
   
        # Search all approvals with project_id
        self._assert_req('/data/search_approvals',  { 'projects_id' : [ self.projects_ids[2] ], 'status' : 'any' }, 
               {u'error': None,
                 u'expences': [],
                 u'trips': [
                         { '_id' : '', "user_id" : self.account_id, 'project_id' : self.projects_ids[2], "description" : "trip2", "status" : 0, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved', 'asd' ], 'accommodation' : {} },    
                         { '_id' : '', "user_id" : self.account_id, 'project_id' : self.projects_ids[2], "description" : "trip3", "status" : -1, "start" : "2010-10-10", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} }     
                            ]
                 }
           )
   
 
 
    def test_approval_search_ok(self):
    
        # Search all with pendance approvation
        self._assert_req('/data/search_approvals',  { 'projects_id' : self.projects_ids }, 
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
                           'user_id': '111111111111111111111111'}],
             'trips': [
                        { '_id' : '', "user_id" : self.account_id, 'project_id' : self.projects_ids[2], "description" : "trip2", "status" : 1, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },    
                       ]}
           )
    
 
        # Search the ones to approve with project_id
        self._assert_req('/data/search_approvals',  { 'projects_id' : [ self.projects_ids[2] ] }, 
               {'error': None,  
             'expences' : [],
             'trips': [
                       { '_id' : '', "user_id" : self.account_id, 'project_id' : self.projects_ids[2], "description" : "trip2", "status" : 1, "start" : "2010-10-08", "end" : "2010-10-10", "country" : "Italy", 'city' : "Rome", 'notes' : [ 'approved' ], 'accommodation' : {} },    
                       ]}
           )
     
        # Search any expences
        self._assert_req('/data/search_approvals',  { 'type' : 'expences', 'status' : 'any', 'projects_id' : self.projects_ids }, 
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
                           'user_id': '111111111111111111111111'}
                                            ], 'trips' : []
                },
           )
      
        # Search all trips
        self._assert_req('/data/search_approvals',  {  'type' : 'trips', 'status' : 'any', 'projects_id' : self.projects_ids }, 
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
                        'user_id': self.account_id},
                        { '_id' : '', 
                         "user_id" : self.account_id, 
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
        self._assert_req('/data/search_approvals',  {  'status' : 'rejected', 'projects_id' : self.projects_ids }, 
               {'error': None,  
             'expences' : [],
             'trips': [
                        { '_id' : '', 
                         "user_id" : self.account_id, 
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
  
  
 
  