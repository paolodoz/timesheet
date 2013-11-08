from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager, clean_id


class CustomerAPIAsAdmin(TestClassBase):
    
    def test_customer_ok(self):
        
        # Remove already unexistant customer
        self._assert_req('/remove/customer', [ { 'name' : 'CUSTOMERTEST' } ], { 'error' : None  })
        
        # Add one customer (return one id)
        customer_json = self._assert_req('/add/customer', [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTO@CUSDOMAIN', 'description' : 'CUSTODESC' } ], { 'error' : None, 'ids' : [ '' ] })
        customer_id = customer_json['ids'][0]
        
        # Get the inserted customer by name
        self._assert_req('/get/customer', [ { 'name' : 'CUSTOMERTEST' }, { 'name' : 1, 'address' : 1, 'phone' : 1, 'contact_person' : 1, 'vat_number' : 1, '_id' : 1, 'website' : 1, 'city' : 1, 'country' : 1, 'postal_code' : 1, 'email' : 1, 'description' : 1 }, { } ], { 'error': None, 'records' : [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', '_id' : '', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTO@CUSDOMAIN', 'description' : 'CUSTODESC'   } ] })
        # Get the inserted customer by id
        self._assert_req('/get/customer', [ { '_id' : customer_id }, { 'address' : 1 }, { }], { 'error': None, 'records' : [ { 'address' : 'CUSTOMER STREET', '_id' : '' } ] })
        # Remove customer by id
        self._assert_req('/remove/customer', [ { '_id' : customer_id } ], { 'error' : None  })
        # Check if collection is empty
        self._assert_req('/get/customer', [ { '_id' : customer_id }, { '_id' : 1 }, { } ], { 'error': None, 'records' : [ ] })


class CustomerAPIAsEmployee(TestCaseAsEmployee):
    
    def test_customer_ko(self):
        self._assert_req('/get/customer', [ {  }, { 'address' : 1 }, { }], { 'error': "TSValidationError: Access to 'get.customer' is restricted for current user", 'records' : [ ] })
        self._assert_req('/remove/customer', [ { 'name' : 'CUSTOMERTEST' } ], {u'error': u"TSValidationError: Access to 'remove.customer' is restricted for current user"})
        self._assert_req('/add/customer', [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTOMAIL@CUSDOMAIN', 'description' : 'CUSTODESC' } ], {u'error': u"TSValidationError: Access to 'add.customer' is restricted for current user", 'ids' : []})
        
        
class CustomerAPIAsManager(TestCaseAsManager):
    
    def test_customer_ok(self):
        self._assert_req('/get/customer', [ {  }, { 'address' : 1 }, { }], { 'error': None, 'records' : [ ] })
        
    
    def test_customer_ko(self):
        self._assert_req('/remove/customer', [ { 'name' : 'CUSTOMERTEST' } ], {u'error': u"TSValidationError: Access to 'remove.customer' is restricted for current user"})
        self._assert_req('/add/customer', [ { 'name' : 'CUSTOMERTEST', 'address' : 'CUSTOMER STREET', 'phone' : '123456789', 'contact_person' : 'CUSTO1', 'vat_number' : 'CUSTOVAT', 'website' : 'CUSTOWEB', 'city' : 'CITY', 'country' : 'COUNTRY', 'postal_code' : '0101', 'email' : 'CUSTOMAIL@CUSDOMAIN', 'description' : 'CUSTODESC' } ], {u'error': u"TSValidationError: Access to 'add.customer' is restricted for current user", 'ids' : []})