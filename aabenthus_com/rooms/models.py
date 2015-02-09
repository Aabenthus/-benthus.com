from django.db import models

class Room(models.Model):
	title = models.CharField(max_length=256)
	location_regexp = models.CharField(max_length=256)
	color = models.CharField(max_length=16)
	glyphicon = models.CharField(max_length=16)
	physical_location = models.CharField(max_length=256)

	def __str__(self):
		return 'Room %s (location matching %s)' % ( self.title, self.location_regexp )

	def slug(self):
		return ''.join(c for c in self.title.lower() if c.isalnum())

	def as_dict(self):
		return dict(
			title = self.title,
			location_regexp = self.location_regexp,
			color = self.color,
			glyphicon = self.glyphicon,
			physical_location = self.physical_location
		)