from django.db import models
from datetime import datetime

class Feedback(models.Model):
	"""
	Feedback
	"""
	feedback = models.CharField(max_length=255)
	user_agent = models.CharField(max_length=255)
	created = models.DateTimeField(default=datetime.now, editable=False)

	class Meta:
		verbose_name = 'Feedback'
		verbose_name_plural = 'Feedback'

	def __unicode__(self):
		return self.feedback