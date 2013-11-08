from testclasses import TestClassBase


class BadRequest(TestClassBase):
    
    def test_bad_add(self):
        self._assert_req('/add/wrong', { 'single': 'dict' }, {'error' : "ValidationError: {u'single': u'dict'} is not of type 'array'", 'ids' : [] })
        self._assert_req('/add/wrong', [ { 'wrong': 'param' } ], {'error' : "KeyError internal exception", 'ids' : [] })
        self._assert_req('/add/user', [ { 'wrong': 'param' } ], {u'error': u"ValidationError: Additional properties are not allowed (u'wrong' was unexpected)", 'ids' : []  })
        self._assert_req('/add/day', [ {u'date': u'2000-10-17', u'UZERZ': [{u'hours': [], u'user_id': u'0'}]} ], { 'error': "ValidationError: Additional properties are not allowed (u'UZERZ' was unexpected)", 'ids' : [] })
        
    def test_bad_get(self):
        
        self._assert_req('/get/user', [ { }, { } ], {u'error': u'ValidationError: [{}, {}] is too short', 'records' : [] })
        self._assert_req('/get/user', [ { }, { }, { }], {u'error': u'ValidationError: {} does not have enough properties', 'records' : [] })
        self._assert_req('/get/user', [ { 'asd': 'ads' }, { }, { 'asd' : 1 } ], {u'error': u'ValidationError: {} does not have enough properties', 'records' : [] })
        
    def test_bad_update(self):
        self._assert_req('/update/user',  [{ '_id' : '1'*24, 'email' : 'CHANGEDEMAIL' } ], { 'error': "ValidationError: [{u'_id': u'111111111111111111111111', u'email': u'CHANGEDEMAIL'}] is not of type 'object'" })
        self._assert_req('/update/user',  { '_id' : '1'*23, 'email' : 'CHANGEDEMAIL' } ,  {u'error': u"ValidationError: u'11111111111111111111111' does not match '[\\\\dabcdef]{24}'"})
        self._assert_req('/update/user',  { 'email' : 'CHANGEDEMAIL' } ,  {u'error': u"ValidationError: '_id' is a required property"})
    
    def test_bad_remove(self):
        self._assert_req('/remove/userZ',  [{ } ], { 'error': "ValidationError: {} does not have enough properties" })
           