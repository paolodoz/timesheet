from testclasses import TestClassBase, TestCaseAsEmployee, TestCaseAsManager
import urllib2

# TODO: add test on manager view as soon as it is ready

class ViewAsAdmin(TestClassBase):
    
     def test_view(self):
        # Search if user management link is displayed
        self.assertRegexpMatches(self._plain_request(), '/index/users')
        
        
class ViewAsEmployee(TestCaseAsEmployee):
    
     def test_view(self):
        # Search if user management link is displayed
        self.assertNotRegexpMatches(self._plain_request(), '/index/users')
        

class ViewAsManager(TestCaseAsManager):
    
     def test_view(self):
        # Search if user management link is displayed
        self.assertNotRegexpMatches(self._plain_request(), '/index/users')