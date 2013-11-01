from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager
from test_report_users_hours import ModuleData

  
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
                                                      'customer' : ''
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', 5*8], [u'2009-10', 100*8]]}
                                    )
        
        # Restrict time span             
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2006-02-02',
                                                      'projects' : [],
                                                      'customer' : ''
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', 5*8]]}
                                    )

        # Restrict projects
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[0] ],
                                                      'customer' : ''
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', 4*5], [U'2009-10', 8*100]]}
                                    )


    def test_report_project_modeproject_ok(self):
          
        self.maxDiff = None
        
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [],
                                                      'customer' : '',
                                                      'mode' : 'project'
                                      }
                                    , {u'error': None, u'records': { self.projects_ids[0] : [[u'2005-10', 20], [u'2009-10', 800]], self.projects_ids[1]: [[u'2005-10', 20]]}}
                                    )
        
        # Restrict time span             
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2006-02-02',
                                                      'projects' : [],
                                                      'customer' : '',
                                                      'mode' : 'project'
                                      }
                                    , {u'error': None,  u'records': { self.projects_ids[0] : [[u'2005-10', 20]], self.projects_ids[1]: [[u'2005-10', 20]]}}
                                    )

        # Restrict projects
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[0] ],
                                                      'customer' : '',
                                                      'mode' : 'project'
                                      }
                                    , {u'error': None, u'records': { self.projects_ids[0] : [[u'2005-10', 20], [u'2009-10', 800]] } }
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
                                                      'customer' : ''
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', 4*5], [U'2009-10', 8*100]]}
                                    )

        # Search by customer
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [  ],
                                                      'customer' : 'CUSTOMER'
                                      }
                                    , {u'error': None, u'records': [[u'2005-10', 4*5], [U'2009-10', 8*100]]}
                                    )
         
    def test_report_project_ko(self):

        # Search without specify project
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-03-03', 
                                                      'end' : '2020-03-03',
                                                      'projects' : [  ],
                                                      'customer' : ''
                                      }
                                    , {u'error': "ValidationError: 'users.hours.project' is a required property" }
                                    )
        
        # Search with wrong project
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [ self.projects_ids[2] ],
                                                      'customer' : ''
                                      }
                                    , {u'error': "ValidationError: u'%s' is not one of ['%s', '%s']" % (self.projects_ids[2], self.projects_ids[0], self.projects_ids[1])}
                                    )
        
        # Search with wrong customer
        self._assert_req('/data/report_projects', {
                                                      'start': '1999-01-01', 
                                                      'end' : '2020-02-02',
                                                      'projects' : [  ],
                                                      'customer' : 'CUSTOMER2'
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
                                                      'customer' : ''
                                      }
                                    , {u'error': "TSValidationError: Action 'report_projects' in 'report_projects' is restricted for current user"}
                                    )  