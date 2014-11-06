from django.db import models


class Deal(models.Model):
	title = models.CharField(max_length=1000)
	price = models.CharField(max_length=10)
	description = models.TextField()
	url = models.URLField(max_length=300)
	date = models.DateField(auto_now=True)

	def __unicode__(self):
		return str(self.date) + '-' + str(self.title)

class GroupDeals(models.Model):
	pass




class Giveaway(models.Model):
	pass
