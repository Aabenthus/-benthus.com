from django.core.management.base import BaseCommand, CommandError
from aabenthus_com.rooms.views import get_credentials, split_events_on_rooms, \
		calculate_conflicts, has_declined_event
from aabenthus_com.google import services
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
	args = ''
	help = 'Notifies any creator of events if they create events that overlaps.'

	def handle(self, *args, **options):
		print("Not yet implemented.")
		'''credentials = get_credentials()
		service = services.calendar(credentials)
		service.watch(calendarId='primary', body={
		  "id": "01234567-89ab-cdef-0123456789ab",
		  "type": "web_hook",
		  "address": reverse(), // Your receiving URL.
		  "expiration": 10
		  }
		});
		'''