from django.test import TestCase

class SampleTestOne(TestCase):
    def testOne(self):
        one = 1
        self.assertEqual(one, 1),
