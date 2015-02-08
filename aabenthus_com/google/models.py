from django.db import models
from oauth2client.django_orm import CredentialsField

import json

class Authorization(models.Model):
	email = models.EmailField(max_length=256, primary_key=True)
	credentials = CredentialsField()
	
	def __str__(self):
		return 'Authorization %s (%s %s)' % (
			self.email,
			'invalid' if self.credentials.invalid else 'valid',
			'with refresh token' if self.credentials.refresh_token else 'without refresh token'
		)