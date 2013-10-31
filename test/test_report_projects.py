from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager
from test_report_users_hours import ModuleData

  
class ReportProjectsAPIAsAdmin(TestClassBase, ModuleData):
      
  
    def setUp(self):        
        TestClassBase.setUp(self)
        ModuleData._add_module_data(self, '1'*24)
      
    def test_day_ok(self):
          
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
