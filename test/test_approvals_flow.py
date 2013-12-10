from testclasses import TestCaseMultipleUsers
from core.config import notifications

def _debug_notification(recipients, notification_type):
    notifications_result = {}
    
    for recipient in recipients:
        notifications_result[recipient['email']] = notifications.get_template('%s.tpl' % notification_type).render(**recipient)
    
    return [ notifications_result ]


   
class FlowAPI(TestCaseMultipleUsers):

    def test_standard_flow(self):
        
        # Add project
        projects_json = self._assert_req('/add/project', [ { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE1' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 
                                                            'responsibles' : [ 
                                                                              { '_id' : self.manager_id, 'name' : 'Manager1', 'role' : 'project manager'}, 
                                                                              { '_id' : self.account_id, 'name' : 'Account1', 'role' : 'account'}
                                                                              ], 
                                                            'employees' : [ { '_id' : self.employee_id, 'name' : 'Employee1'} ], } 
                                 ], 
                { 'error' : None, 'ids' : [ '' ] }
                )
        self.projects_ids = projects_json['ids']
        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }  ], { 'error' : None }))
        
        ### EMPLOYEE
        self._log_as_employee()
        # Push new expence
        expence_json = self._assert_req('/data/push_expences', [ 
                         { '_id' : self.projects_ids[0], 
                          "expences" : [ 
                                         { "user_id" : self.employee_id, "trip_id" : '2'*24, 'status': 3, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }     
                         ] } ], { 'error' : None, 'ids' : [ '' ] } )
        expence_ids = expence_json['ids']
        
        # Submit to approval flow (pm)
        self._assert_req('/data/approval',  { 'user_id' : self.employee_id, 'project_id' : self.projects_ids[0], 'expence_id' : expence_ids[0], 'action' : 'approve', 'note' : 'asd2'  }, 
               { 'error' : None, 'status' : 2, 'notifications' : _debug_notification(self.manager_data, 'notify_new') }
        )
        
        ### PROJECT MANAGER
        self._log_as_manager()
        # Submit to account
        self._assert_req('/data/approval',  { 'user_id' : self.employee_id, 'project_id' : self.projects_ids[0], 'expence_id' : expence_ids[0], 'action' : 'approve', 'note' : 'asd2'  }, 
               { 'error' : None, 'status' : 1, 'notifications' : _debug_notification(self.account_data, 'notify_new') }
        )      

        ### ACCOUNT
        self._log_as_account()
        # Submit to account
        self._assert_req('/data/approval',  { 'user_id' : self.employee_id, 'project_id' : self.projects_ids[0], 'expence_id' : expence_ids[0], 'action' : 'approve', 'note' : 'asd2'  }, 
               { 'error' : None, 'status' : 0, 'notifications' : _debug_notification(self.employee_data, 'notify_new') }
        )  
        
        ### EMPLOYEE
        self._log_as_employee()
        self._assert_req('/data/search_approvals', { 'user_id': self.employee_id, 'projects_id' : self.projects_ids, 'status' : 'approved' }, { 'error' : None, 'expences' : [ 
                   { "project_id" : self.projects_ids[0], 
                    '_id' : '', 
                    "user_id" : self.employee_id, 
                    "trip_id" : '2'*24, 
                    'status': 0, 
                    "date" : "2005-10-08", 
                    "file" : {}, 
                    'objects' : [{}],
                    'notes' : [u'asd2', u'asd2', u'asd2']
                    }],
                    'trips': []
              })

    def test_standard_reject(self):
        
        # Add project
        projects_json = self._assert_req('/add/project', [ { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE1' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 
                                                            'responsibles' : [ 
                                                                              { '_id' : self.manager_id, 'name' : 'Manager1', 'role' : 'project manager'}, 
                                                                              { '_id' : self.account_id, 'name' : 'Account1', 'role' : 'account'}
                                                                              ], 
                                                            'employees' : [ { '_id' : self.employee_id, 'name' : 'Employee1'} ], } 
                                 ], 
                { 'error' : None, 'ids' : [ '' ] }
                )
        self.projects_ids = projects_json['ids']
        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }  ], { 'error' : None }))
        
        ### EMPLOYEE
        self._log_as_employee()
        # Push new expence
        expence_json = self._assert_req('/data/push_expences', [ 
                         { '_id' : self.projects_ids[0], 
                          "expences" : [ 
                                         { "user_id" : self.employee_id, "trip_id" : '2'*24, 'status': 3, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }     
                         ] } ], { 'error' : None, 'ids' : [ '' ] } )
        expence_ids = expence_json['ids']
        
        # Submit to approval flow (pm)
        self._assert_req('/data/approval',  { 'user_id' : self.employee_id, 'project_id' : self.projects_ids[0], 'expence_id' : expence_ids[0], 'action' : 'approve', 'note' : 'asd2'  }, 
               { 'error' : None, 'status' : 2, 'notifications' : _debug_notification(self.manager_data, 'notify_new') }
        )
        
        ### PROJECT MANAGER
        self._log_as_manager()
        # Submit to account
        self._assert_req('/data/approval',  { 'user_id' : self.employee_id, 'project_id' : self.projects_ids[0], 'expence_id' : expence_ids[0], 'action' : 'reject', 'note' : 'asd2'  }, 
               { 'error' : None, 'status' : -2, 'notifications' : _debug_notification(self.employee_data, 'notify_reject') }
        )      

        ### EMPLOYEE
        self._log_as_employee()
        self._assert_req('/data/search_approvals', { 'user_id': self.employee_id, 'projects_id' : self.projects_ids, 'status' : 'rejected' }, { 'error' : None, 'expences' : [ 
                   { "project_id" : self.projects_ids[0], 
                    '_id' : '', 
                    "user_id" : self.employee_id, 
                    "trip_id" : '2'*24, 
                    'status': -2, 
                    "date" : "2005-10-08", 
                    "file" : {}, 
                    'objects' : [{}],
                    'notes' : [u'asd2', u'asd2']
                    }],
                    'trips': []
              })


    def test_draft(self):
        
        # Add project
        projects_json = self._assert_req('/add/project', [ { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE1' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 
                                                            'responsibles' : [ 
                                                                              { '_id' : self.manager_id, 'name' : 'Manager1', 'role' : 'project manager'}, 
                                                                              { '_id' : self.account_id, 'name' : 'Account1', 'role' : 'account'}
                                                                              ], 
                                                            'employees' : [ { '_id' : self.employee_id, 'name' : 'Employee1'} ], } 
                                 ], 
                { 'error' : None, 'ids' : [ '' ] }
                )
        self.projects_ids = projects_json['ids']
        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }  ], { 'error' : None }))
        
        ### EMPLOYEE
        self._log_as_employee()
        # Push new expence without submit
        expence_json = self._assert_req('/data/push_expences', [ 
                         { '_id' : self.projects_ids[0], 
                          "expences" : [ 
                                         { "user_id" : self.employee_id, "trip_id" : '2'*24, 'status': 3, "date" : "2005-10-08", "file" : {}, 'objects' : [{}] }     
                         ] } ], { 'error' : None, 'ids' : [ '' ] } )
        expence_ids = expence_json['ids']
        
        ### PROJECT MANAGER
        self._log_as_manager()
        # Search but is unreachable
        self._assert_req('/data/search_approvals', { 'projects_id' : self.projects_ids, 'status' : 'any' }, {u'error': u'TSValidationError: Empty list found validating current user request'})    

        ### ACCOUNT
        self._log_as_account()
        # Search but is unreachable
        self._assert_req('/data/search_approvals', { 'projects_id' : self.projects_ids, 'status' : 'any' }, {u'error': u'TSValidationError: Empty list found validating current user request'})    



        ### EMPLOYEE
        self._log_as_employee()
        self._assert_req('/data/search_approvals', { 'user_id': self.employee_id, 'projects_id' : self.projects_ids, 'status' : 'any' }, { 'error' : None, 'expences' : [ 
                   { 
                    '_id' : '',
                   "project_id" : self.projects_ids[0], 
                   "user_id" : self.employee_id, 
                   "trip_id" : '2'*24, 
                   'status': 3, 
                   "date" : "2005-10-08", 
                   "file" : {}, 
                   'objects' : [{}] } ],
                    'trips': []
              })

