from django.test import TestCase


class FeedbackViewsTestCase(TestCase):
	def test_index(self):
		resp = self.client.get('/feedback/')
		self.assertEqual(resp.status_code, 200)
