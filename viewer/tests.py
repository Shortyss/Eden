from django.test import TestCase

# Create your tests here.


class ExampleTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up data for all class methods")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup data")
        pass

    def test_false(self):
        print("Test method: test_false")
        self.assertFalse(False)