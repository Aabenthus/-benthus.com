from django.db import models

class Room(models.Model):
	title = models.CharField(max_length=256)
	location_regexp = models.CharField(max_length=256)
	color = models.CharField(max_length=16)
	glyphicon = models.CharField(max_length=16)

	def __str__(self):
		return 'Room %s (location matching %s)' % ( self.title, self.location_regexp )

	def as_dict(self):
		return dict(
			title = self.title,
			location_regexp = self.location_regexp,
			color = self.color,
			glyphicon = self.glyphicon
		)