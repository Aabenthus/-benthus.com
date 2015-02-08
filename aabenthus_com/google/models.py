from django.db import models
from oauth2client.django_orm import CredentialsField

import json

class Authorization(models.Model):
	email = models.EmailField(max_length=256, primary_key=True)
	credentials = CredentialsField()
	
	def __str__(self):
		return 'Authorization %s' % ( self.email )