from django.db import models

class Authorization(models.Model):
	email = models.CharField(max_length=256)
	credentials = models.CharField(max_length=1024)
	
	def __str__(self):
		return 'Authorization %s' % ( self.email )