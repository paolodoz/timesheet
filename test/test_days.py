from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager


class DayAPIAsAdmin(TestClassBase):
    
    def test_day_ok(self):
        
        # Insert a day without user
        self._assert_req('/data/push_days', [ {'date': '2000-01-01' }
                                    ], { 'error' : None })   
        # Insert wrongly a day with multiple users
        self._assert_req('/data/push_days', [ {'date': '2000-01-01', 
                                      'users': [ 
                                                { 'user_id' : '111111111111111111111111', 
                                                 'hours': []
                                                 },
                                                 { 'user_id' : '0', 
                                                 'hours': []
                                                 } 
                                                ]
                                      }
                                    ], { 'error' : 'TSValidationError: Push only one user per day' })
        
    def test_day_ko(self):
        # Insert the day 17 for user  '111111111111111111111111'                                      
        self._assert_req('/data/push_days', [ {'date': '2000-10-17', 
                                      'users': [ 
                                                { 'user_id' : '111111111111111111111111', 
                                                 'hours': [
                                                           {u'note': u'FIRST 4 HOURS', u'task': 0, u'isextra': False, u'project': u'524efeef2c066a1bc6000001', u'amount': 4}, 
                                                           {u'note': u'SECOND 4 HOURS', u'task': 0, u'isextra': False, u'project': u'524efeef2c066a1bc6000001', u'amount': 4}
                                                           ]
                                                 }
                                                ]
                                      }
                                    ], { 'error' : None })   
        # Push in the day 17 also user  '0'                                      
        self._assert_req('/data/push_days', [ {'date': '2000-10-17', 
                                      'users': [ 
                                                { 'user_id' : '0', 
                                                 'hours': []
                                                 }
                                                ]
                                      }
                                    ], { 'error' : None })                                            
        # Push also the year after the user  '0'                                      
        self._assert_req('/data/push_days', [ {'date': '2001-02-02', 
                                      'users': [ 
                                                { 'user_id' : '0', 
                                                 'hours': []
                                                 }
                                                ]
                                      }
                                    ], { 'error' : None })   
        # Get the day 2000-10-17 for user 0                                        
        self._assert_req('/data/search_days', { 'date_from' : '2000-10-17', 'date_to' : '2000-10-17', 'user_id' : '0' }, {u'records': [{u'date': u'2000-10-17', u'_id': '', u'users': [{u'hours': [], u'user_id': u'0'}]}], u'error': None})
        # Get the years 2000-01-01 2003-01-01 for user 0
        self._assert_req('/data/search_days', { 'date_from' : '2000-01-01', 'date_to' : '2003-01-01', 'user_id' : '0' }, {u'records': [{u'date': u'2000-10-17', u'_id': '', u'users': [{u'hours': [], u'user_id': u'0'}]}, {u'date': u'2001-02-02', u'_id': '', u'users': [{u'hours': [], u'user_id': u'0'}]}], u'error': None} )
        # Get unexistant user 2
        self._assert_req('/data/search_days', { 'date_from' : '2000-01-01', 'date_to' : '2003-01-01', 'user_id' : '2' }, {u'records': [ ], u'error': None} )
        # Get empty span 
        self._assert_req('/data/search_days', { 'date_from' : '2010-01-01', 'date_to' : '2011-01-01', 'user_id' : '0' }, {u'records': [ ], u'error': None} )
        # Delete all inserted days
        self._assert_req('/remove/day', [ { "date" :  "2000-10-17" },  { "date" :  "2000-01-01" },  { "date" :  "2001-02-02" } ] , { 'error' : None })
        

class DayAPIAsEmployee(TestCaseAsEmployee):
    
    def test_day_ko(self):
        # Access directly to /day/
        self._assert_req('/get/day', [ {  }, { 'date' : '2000-01-01' } ], {u'error': u"TSValidationError: Action 'get' in 'day' is restricted for current user", 'records' : [] } )
    
    def test_day_ko(self):
        
        # Get unexistant user 0
        self._assert_req('/data/search_days', { 'date_from' : '2000-01-01', 'date_to' : '2003-01-01', 'user_id' : '0' }, {u'error': u"ValidationError: Error '0' is not valid"} )
        # Get admin days 
        self._assert_req('/data/search_days', { 'date_from' : '2000-01-01', 'date_to' : '2003-01-01', 'user_id' : '111111111111111111111111' }, {u'error': u"ValidationError: Error '111111111111111111111111' is not valid"} )
        # TODO: add search days per project
        
        
        # Insert a day without user
        self._assert_req('/data/push_days', [ {'date': '2000-01-01' } ], { 'error' : None })   
        # Insert a day with the user_id of admin
        self._assert_req('/data/push_days', [ {'date': '2000-10-17', 'users': [ { 'user_id' : '111111111111111111111111', 'hours': [] } ] } ], {u'error': u"ValidationError: Error '111111111111111111111111' is not valid"})    
        
        
class DayAPIAsManager(TestCaseAsManager):
    def test_day_ko(self):
        
        # Access directly to /day/
        self._assert_req('/get/day', [ {  }, { 'date' : '2000-01-01' } ], {u'error': u"TSValidationError: Action 'get' in 'day' is restricted for current user", 'records' : [] } )
        
        
        # Get wrong user_id 0
        self._assert_req('/data/search_days', { 'date_from' : '2000-01-01', 'date_to' : '2003-01-01', 'user_id' : '0' }, {u'error': u"ValidationError: Error '0' is not valid"} )
        # Get admin days 
        self._assert_req('/data/search_days', { 'date_from' : '2000-01-01', 'date_to' : '2003-01-01', 'user_id' : '111111111111111111111111' }, {u'error': u"ValidationError: Error '111111111111111111111111' is not valid"} )
        
        # Insert day with wrong user_id
        self._assert_req('/data/push_days', [ {'date': '2001-02-02', 
                              'users': [ 
                                        { 'user_id' : '0', 
                                         'hours': []
                                         }
                                        ]
                              }
                            ], { u'error': u"ValidationError: Error '0' is not valid" })  
           
        # Insert day with right userid but random project
        self._assert_req('/data/push_days', [ {'date': '2000-10-17', 
                                      'users': [ 
                                                { 'user_id' : self.manager_id, 
                                                 'hours': [
                                                           {u'note': u'FIRST 4 HOURS', u'task': 0, u'isextra': False, u'project': u'7'*24, u'amount': 4}, 
                                                           ]
                                                 }
                                                ]
                                      }
                                    ], {u'error': u"ValidationError: Error '%s' is not valid" % ('7'*24)})   
           
                
    def test_day_ok(self):
        
        # Insert day with right user_id
        self._assert_req('/data/push_days', [ {'date': '2001-02-02', 
                              'users': [ 
                                        { 'user_id' : self.manager_id, 
                                         'hours': []
                                         }
                                        ]
                              }
                            ], { u'error': None })  
           
        # Insert day with right project
        self._assert_req('/data/push_days', [ {'date': '2000-10-17', 
                                      'users': [ 
                                                { 'user_id' : self.manager_id, 
                                                 'hours': [
                                                           {u'note': u'FIRST 4 HOURS', u'task': 0, u'isextra': False, u'project': self.managed_projects[0], u'amount': 4}, 
                                                           ]
                                                 }
                                                ]
                                      }
                                    ], {u'error': None})   


