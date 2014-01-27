from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager, clean_id


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
                                 { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person1', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : current_id, 'name' : 'Manag1', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ] },
                                 { 'customer' : 'CUSTOMER1', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME2', 'description' : 'description', 'contact_person' : 'contact_person2', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : self.users_ids[0], 'name' : 'Manag2', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[0], 'name' : 'Emp2'} ] }, 
                                 { 'customer' : 'CUSTOMER3', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME3', 'description' : 'description', 'contact_person' : 'contact_person3', 'start' : '2003-04-05', 'end' : '2010-05-06', 'tasks' : [ 2, 3 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : self.users_ids[1], 'name' : 'Manag3', 'role' : 'project manager'} ], 'employees' : [ { '_id' : current_id, 'name' : 'Emp3'} ] } 
                                 ], 
                { 'error' : None, 'ids' : [ '', '', '' ] }
                )
        self.projects_ids = projects_json['ids']
        self.execOnTearDown.append(('/remove/project', [ { '_id' : self.projects_ids[0]  }, { '_id' : self.projects_ids[1] }, { '_id' : self.projects_ids[2] }  ], { 'error' : None }))
 

class ProjectsAPIAsAdmin(TestClassBase, ModuleData):

    def setUp(self):        
        TestClassBase.setUp(self)
        ModuleData._add_module_data(self, '1'*24)
    
    def test_project_ok(self):
        
        # Remove already unexistant project
        self._assert_req('/remove/project', [ { 'name' : 'PROJECTZ'  } ], { 'error' : None  })
        # Get the inserted project by NAME
        self._assert_req('/get/project', [ { 'name' : 'PROJECTNAME1' }, { 'contact_person' : 1, '_id' : 0 }, { } ], { 'error': None, 'records' : [ { 'contact_person' : 'contact_person1'  } ] })
        # Get the inserted project by responsible
        self._assert_req('/get/project', [ { 'responsibles._id' : self.users_ids[1]  }, { 'name' : 1, '_id' : 0 }, { } ], { 'error': None, 'records' : [ { 'name' : 'PROJECTNAME3'  } ] })
        # Get the inserted project by employers
        self._assert_req('/get/project', [ { 'employees._id' : self.users_ids[0] } , { 'name' : 1, '_id' : 0 }, { } ], { 'error': None, 'records' : [ { 'name' : 'PROJECTNAME2'  } ] })
        # Get projects with reverse ordering by name
        self._assert_req('/get/project', [ { } , { 'name' : 1, '_id' : 0 }, { 'name' : -1 } ], { 'error': None, 'records' : [ { 'name' : 'PROJECTNAME3' }, { 'name' : 'PROJECTNAME2' }, { 'name' : 'PROJECTNAME1' } ] })
        
    def test_project_types_ko(self):
        
        # Wrong type on main project struct
        self._assert_req('/add/project', [ 
             { 'customer' : 'CUSTOMER4', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME4', 'description' : 'description4', 'contact_person' : 'contact_person4', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : '1'*24, 'name' : 3, 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ] },
             ], 
        {u'error': u"ValidationError: 3 is not of type 'string'", u'ids': []}
        )
         
        # Wrong type on main project struct
        self._assert_req('/add/project', [ 
             { 'customer' : 'CUSTOMER4', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME4', 'description' : 'description4', 'contact_person' : 'contact_person4', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : '1'*24, 'name' : 'resp1', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ],
              u'economics': [{u'note': u'dsffdsfds', u'extra': 4242, u'period': u'2013-11-26', u'budget': 'STR', u'invoiced': 0}, {u'note': u'das', u'extra': 5, u'invoiced': 0, u'period': u'2013-11-26', u'budget': 4}] },
             ], 
        {u'error': u"ValidationError: u'STR' is not of type 'number'", u'ids': []}
        )
        
        # Wrong type on main project struct on UPDATE
        self._assert_req('/update/project',  
             { '_id' : self.projects_ids[0], u'economics': [{u'note': u'dsffdsfds', u'extra': 4242, u'period': u'2013-11-26', u'budget': 'STR_NOT_INT', u'invoiced': 0}, {u'note': u'das', u'extra': 5, u'invoiced': 0, u'period': u'2013-11-26', u'budget': 4}] },
             {u'error': u"ValidationError: u'STR_NOT_INT' is not of type 'number'"}
        )


        # Wrong responsible role
        self._assert_req('/add/project', [ 
                                 { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person1', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : '1'*24, 'name' : 'Manag1', 'role' : 'ROLEZ'} ], 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ] },
                                 ], 
                { 'error' : "ValidationError: u'ROLEZ' is not one of ['administrator', 'employee', 'project manager', 'account']", 'ids' : [  ] }
        )

    def test_project_flow_ok(self):
        self._assert_req('/update/project',  
             { '_id' : self.projects_ids[0], 'expences' : [ 
                                                 { '_id' : '6'*24, "user_id" : '1'*24, "trip_id" : '3'*24, 'status' : 0, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2005-10-04', 'amount' : 5}, { 'date' : '2000-01-05', 'amount' : 10}] },
                                                 # Following expence is not approved     
                                                 { '_id' : '5'*24, "user_id" : '1'*24, "trip_id" : '4'*24, 'status' : 2, "date" : "2010-10-09", "file" : {}, 'objects' : [{ 'date' : '2005-10-09', 'amount' : 5}, { 'date' : '2000-01-09', 'amount' : 10}] }     
                                 ]
              }, {u'error': None}
        )
        
class ReportUsersHoursAPIAsManager(TestCaseAsManager, ModuleData):
    
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.manager_id)
        self._log_as_user()
        
    def test_project_ko(self):

        # Get the project without specify responsibles._id or employees._id
        self._assert_req('/get/project', [ { 'name' : 'PROJECTNAME1'}, { 'contact_person' : 1, '_id' : 0 }, { } ], { 'error': "ValidationError: {u'name': u'PROJECTNAME1'} is not valid under any of the given schemas", 'records' : [ ] })
        # Get the project specifying wrong responsibles._id
        self._assert_req('/get/project', [ { 'responsibles._id' : self.users_ids[1]  }, { 'name' : 1, '_id' : 0 }, { } ], { 'error': "ValidationError: {u'responsibles._id': u'%s'} is not valid under any of the given schemas" % self.users_ids[1], 'records' : [ ] })
        # Get the project specifying wrong employees._id
        self._assert_req('/get/project', [ { 'employees._id' : self.users_ids[0] } , { 'name' : 1, '_id' : 0 }, { } ], { 'error': "ValidationError: {u'employees._id': u'%s'} is not valid under any of the given schemas" % self.users_ids[0], 'records' : [ ] })
        # Get the project specifying wrongly both
        self._assert_req('/get/project', [ { 'employees._id' : self.manager_id, 'responsibles._id' : self.manager_id } , { 'name' : 1, '_id' : 0 }, { } ], {u'error': "ValidationError: {u'responsibles._id': u'%s', u'employees._id': u'%s'} is valid under each of {'required': ['responsibles._id'], 'type': 'object', 'properties': {'responsibles._id': {'pattern': '^%s$', 'type': 'string'}}}, {'required': ['employees._id'], 'type': 'object', 'properties': {'employees._id': {'pattern': '^%s$', 'type': 'string'}}}" % (self.manager_id, self.manager_id, self.manager_id, self.manager_id), u'records': []})
        
        # Try to delete
        self._assert_req('/remove/project', [ { '_id' : self.projects_ids[0], 'responsibles._id' : self.manager_id } ], { 'error': "TSValidationError: Access to 'remove.project' is restricted for current user" })
        
        # Try to insert
        self._assert_req('/add/project', [ { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person1', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : self.users_ids[1], 'name' : 'Manag1', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ] } ], 
                { 'error' : "TSValidationError: Access to 'add.project' is restricted for current user", 'ids' : [  ] }
                )

        # Update project that does not manage
        self._assert_req('/update/project', { '_id' : self.projects_ids[1], 'customer' : 'CUSTOMERZ', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person1', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : self.manager_id, 'name' : 'Manag1', 'role' : 'project manager' } ], 'employees' : [ { '_id' : self.manager_id, 'name' : 'Emp1'} ] },  { 'error' : "ValidationError: u'%s' is not one of ['%s']" % (self.projects_ids[1], str(self.projects_ids[0]) ) } )
        
        
        
    def test_project_ok(self):

        # Get the project specifying responsibles._id as current user
        self._assert_req('/get/project', [ { 'responsibles._id' : self.manager_id  }, { 'name' : 1, '_id' : 0 }, { } ], {u'error': None, u'records': [{u'name': u'PROJECTNAME1'}]})
        # Get the project  specifying employees._id as current user
        self._assert_req('/get/project', [ { 'employees._id' : self.manager_id } , { 'name' : 1, '_id' : 0 }, { } ], {u'error': None, u'records': [{u'name': u'PROJECTNAME3'}]})
        # Get the project specifying employer and manager
        self._assert_req('/get/project', [ { 'employees._id' : self.users_ids[1], 'responsibles._id' : self.manager_id } , { 'name' : 1, '_id' : 0 }, { } ], {u'error': None, u'records': [{u'name': u'PROJECTNAME1'}]})
        
        # Update first project
        self._assert_req('/update/project', { '_id' : self.projects_ids[0], 'customer' : 'CUSTOMERZ', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person1', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : self.manager_id, 'name' : 'Manag1', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.manager_id, 'name' : 'Emp1'} ] },  { 'error' : None } )
        self._assert_req('/get/project', [ { '_id' : self.projects_ids[0], 'responsibles._id' : self.manager_id } , { 'customer' : 1, '_id' : 0 }, { } ], {u'error': None, u'records': [{u'customer': u'CUSTOMERZ'}]})
        
    def test_project_flow_ko(self):
        self._assert_req('/update/project',  
             { '_id' : self.projects_ids[0], 'expences' : [ 
                                                 { '_id' : '6'*24, "user_id" : '1'*24, "trip_id" : '3'*24, 'status' : 0, "date" : "2010-10-08", "file" : {}, 'objects' : [{ 'date' : '2005-10-04', 'amount' : 5}, { 'date' : '2000-01-05', 'amount' : 10}] },
                                                 # Following expence is not approved     
                                                 { '_id' : '5'*24, "user_id" : '1'*24, "trip_id" : '4'*24, 'status' : 2, "date" : "2010-10-09", "file" : {}, 'objects' : [{ 'date' : '2005-10-09', 'amount' : 5}, { 'date' : '2000-01-09', 'amount' : 10}] }     
                                 ]
              }, {u'error': u'ValidationError: 0.0 is less than the minimum of 2'}
        )

class ReportUsersHoursAPIAsEmployee(TestCaseAsEmployee, ModuleData):
    
    def setUp(self):        
        TestClassBase.setUp(self)
        self._add_user_data()
        ModuleData._add_module_data(self, self.employee_id)
        self._log_as_user()
        
    def test_project_ko(self):

        # Get the project without specify responsibles._id or employees._id
        self._assert_req('/get/project', [ { 'name' : 'PROJECTNAME1'}, { 'contact_person' : 1, '_id' : 0 }, { } ], { 'error': "ValidationError: 'employees._id' is a required property", 'records' : [ ] })
        # Get the project specifying wrong employees._id
        self._assert_req('/get/project', [ { 'employees._id' : self.users_ids[0] } , { 'name' : 1, '_id' : 0 }, { } ], { 'error': "ValidationError: u'%s' does not match '^%s$'" % (self.users_ids[0], self.employee_id), 'records' : [ ] })
        
        # Try to delete
        self._assert_req('/remove/project', [ { 'employees._id' : self.users_ids[0] } ], { 'error': "TSValidationError: Access to 'remove.project' is restricted for current user" })
         
        # Try to insert
        self._assert_req('/add/project', [ { 'customer' : 'CUSTOMER', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person1', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' :  [ { '_id' : self.users_ids[1], 'name' : 'Manag1', 'role' : 'project manager'} ], 'employees' : [ { '_id' : self.users_ids[1], 'name' : 'Emp1'} ] } ], 
                { 'error' : "TSValidationError: Access to 'add.project' is restricted for current user", 'ids' : [  ] }
                )
 
        # Update project 
        self._assert_req('/update/project', { '_id' : self.projects_ids[0], 'customer' : 'CUSTOMERZ', 'tags' : [ 'TYPE' ], 'name' : 'PROJECTNAME1', 'description' : 'description', 'contact_person' : 'contact_person1', 'start' : '2000-01-02', 'end' : '2006-02-03', 'tasks' : [ 1, 2 ], 'grand_total' : 4, 'responsibles' : [ { '_id' : self.employee_id, 'name' : 'Manag1', 'role' : 'project manager' } ], 'employees' : [ { '_id' : self.employee_id, 'name' : 'Emp1'} ] },  { 'error' : "TSValidationError: Access to 'update.project' is restricted for current user" } )
         

    def test_project_ok(self):
 
        # Get the project  specifying employees._id as current user
        self._assert_req('/get/project', [ { 'employees._id' : self.employee_id } , { 'name' : 1, '_id' : 0 }, { } ], {u'error': None, u'records': [{u'name': u'PROJECTNAME3'}]})
        # Get the project specifying employer and manager
        self._assert_req('/get/project', [ { 'employees._id' : self.employee_id, 'responsibles._id' : self.users_ids[1] } , { 'name' : 1, '_id' : 0 }, { } ], {u'error': None, u'records': [{u'name': u'PROJECTNAME3'}]})
        # Get the project specifying right employer and wrong manager
        self._assert_req('/get/project', [ { 'employees._id' : self.employee_id, 'responsibles._id' : self.users_ids[2] } , { 'name' : 1, '_id' : 0 }, { } ], {u'error': None, u'records': [ ]})

         