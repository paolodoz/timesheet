from testclasses import TestClassBase


class BadRequest(TestClassBase):
    
    def test_basic_bad(self):
        
        # Add directly json without list
        self._assert_req('/add/wrong', { 'single': 'dict' }, {'error' : "TSValidationError: List expected, not 'dict'", 'ids' : [] })
        # Add unexistant collection
        self._assert_req('/add/wrong', [ { 'wrong': 'param' } ], {'error' : "KeyError internal exception", 'ids' : [] })
        # Add user with unsupported param 
        self._assert_req('/add/user', [ { 'wrong': 'param' } ], {u'error': u"ValidationError: Error '{u'wrong': u'param'}' is not valid", 'ids' : []  })
        # Get without a valid projection
        self._assert_req('/get/user', [ { }, { } ], { 'error': 'TSValidationError: Expected list with criteria and nonempty projection', 'records' : [] })
        # Get badly formatted
        self._assert_req('/add/day', [ {u'date': u'2000-10-17', u'UZERZ': [{u'hours': [], u'user_id': u'0'}]} ], { 'error': "ValidationError: Error '{u'date': u'2000-10-17', u'UZERZ': [{u'hours': [], u'user_id': u'0'}]}' is not valid", 'ids' : [] })
        