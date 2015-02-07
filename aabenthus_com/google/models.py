from django.db import models

import json

class Authorization(models.Model):
	email = models.CharField(max_length=256)
	credentials = models.TextField()
	
	def __str__(self):
		return 'Authorization %s' % ( self.email )

	def refresh_if_needed(self):
		credentials = json.loads(self.credentials)
		print(credentials.get('refresh_token'))
		pass