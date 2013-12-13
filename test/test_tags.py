from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager, clean_id


class ModuleData:

    def _add_module_data(self, current_id):
        
        # Add projects
        projects_json = self._assert_req('/add/project', [ 
                                 { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE1' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person1', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag1', 'role' : 'project manager'} ], 'employees' : [ ] },
                                 { 'customer' : 'CUSTOMER1', 'tags' : [ 'TYPE2', 'TYPE1' ], 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person2', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag2', 'role' : 'project manager' } ], 'employees' : [ { '_id' : current_id, 'name' : 'Emp2'} ] }, 
                                 { 'customer' : 'CUSTOMER3', 'tags' : [ 'TYPE3' ], 'name' : 'PROJECTNAME3', 'description' : 'description', 'contact_person' : 'contact_person3', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ ], 'employees' : [  ] },
                                 { 'customer' : 'CUSTOMER4', 'tags' : [ 'TYPE1', 'TYPE4' ], 'name' : 'PROJECTNAME4', 'description' : 'description', 'contact_person' : 'contact_person4', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [], 'employees' : [  ] } 
                                 ], 
                { 'error' : None, 'ids' : [ '', '', '', '' ] }
                )
        self.projects_ids = projects_json['ids']
        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }, { '_id' : self.projects_ids[1] }, { '_id' : self.projects_ids[2] }, { '_id' : self.projects_ids[3] }  ], { 'error' : None }))
 

class TagAPIAsAdmin(TestClassBase, ModuleData):

    def setUp(self):        
        TestClassBase.setUp(self)
        ModuleData._add_module_data(self, '1'*24)
    
    def test_tag_ok(self):
        # Get first 2 tags
        self._assert_req('/data/search_tags', { 'count' : 2  }, {u'error': None, u'records': [u'TYPE1', u'TYPE4' ]})
        
        # Get first 100 tags
        self._assert_req('/data/search_tags', { 'count' : 100  }, {u'error': None, u'records': [u'TYPE1', u'TYPE3', u'TYPE4', u'TYPE2']})
        
        
    def test_tag_ko(self):
        # Insert non unique tags
        self._assert_req('/add/project', [ { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE1', 'TYPE1' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person1', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : '1'*24, 'name' : 'Manag1', 'role' : 'project manager'} ], 'employees' : [ ] } ], { 'error' : "ValidationError: [u'TYPE1', u'TYPE1'] has non-unique elements", 'ids' : [ ] })

        
class TagAPIAsManager(TestCaseAsManager, ModuleData):
    
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.manager_id)
        self._log_as_user()
     
    def test_tag_ok(self):
        # Get first 3 tags
        self._assert_req('/data/search_tags', { 'count' : 3  }, {u'error': None, u'records': [u'TYPE1', u'TYPE4',  u'TYPE3' ]})
        

class TagAPIAsEmployee(TestCaseAsEmployee, ModuleData):
    
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.employee_id)
        self._log_as_user()
        
    def test_tag_ko(self):
        # Get first 3 tags
        self._assert_req('/data/search_tags', { 'count' : 3  }, {u'error': u"TSValidationError: Access to 'search_tags' is restricted for current user"})
        