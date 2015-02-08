from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.mail import EmailMultiAlternatives

from django.utils import timezone
from datetime import timedelta
import dateutil.parser
import json
from oauth2client import client
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.django_orm import Storage
import re

from aabenthus_com.google import services
from aabenthus_com.google.models import Authorization

from .models import Room

def get_credentials():
	storage = Storage(Authorization, 'email', settings.ROOMS_EMAIL, 'credentials')
	return storage.get()

def split_events_on_rooms(events):
	result = list()
	rooms = Room.objects.all()
	for room in rooms:
		room_dict = room.as_dict()
		room_location_regexp = re.compile(room.location_regexp, re.IGNORECASE)
		room_dict['events'] = filter_events_by_room(events, room_location_regexp)
		result.append(room_dict	)
	return result

def filter_events_by_room(events, room_location_regexp):
	result = list()
	for event in events:
		location = event.get('location') or ''
		if room_location_regexp.match( location ):
			result.append(event)
	return result

def calculate_conflicts(rooms):
	for room in rooms:
		# TODO: Implement something smarter than an n^2 algorithm
		for event1 in room.get('events'):
			for event2 in room.get('events'):
				different = event1 is not event2
				event1_ends_efter_event2_starts = event1.get('end') > event2.get('start')
				event1_starts_before_event2_ends = event1.get('starts') < event2.get('end')
				if different and event1_ends_efter_event2_starts and event1_starts_before_event2_ends:
					event1_created = dateutil.parser.parse( event1.get('created') )
					event2_created = dateutil.parser.parse( event2.get('created') )
					if event1_created > event2_created:
						event1['conflicts'] = True
						event1['conflicts_with'] = event2
					else:
						event2['conflicts'] = True
						event2['conflicts_with'] = event1
	return rooms

def send_conflict_mail(event, room):
	organizers_email = event.get('organizer').get('email')
	text_data = (
		settings.ROOMS_EMAIL,
		room.get('title'),
		event.get('conflicts_with').get('organizer').get('displayName')
	)
	text_content = '''You have invited %s for an event in %s, but %s beat you too it.\n
Please update your event by choosing a different location or time.''' % text_data
	# html_content = '<p>This is an <strong>important</strong> message.</p>'

	msg = EmailMultiAlternatives(settings.CONFLICT_MAIL_SUBJECT % event.get('summary'),
		text_content, settings.CONFLICT_MAIL_FROM, [organizers_email])
	#msg.attach_alternative(html_content, "text/html")
	msg.send()

def decline_conflicting_event(event, room):
	credentials = get_credentials()
	service = services.calendar(credentials)

	for attendee in event.get('attendees'):
		if attendee['self']:
			attendee['responseStatus'] = 'declined'

	service.events().update(
		calendarId='primary',
		eventId=event['id'],
		body=event
	).execute()

def has_declined_event(event):
	if event.get('attendees'):
		for attendee in event.get('attendees'):
			if attendee['self']:
				if attendee['responseStatus'] == 'declined':
					return True
	return False

def list_bookings(request, timeMin = None, timeMax = None):
	credentials = get_credentials()
	service = services.calendar(credentials)

	if timeMin:
		timeMin = dateutil.parser.parse(timeMin)
	else:
		timeMin = timezone.now()
		timeMin = timeMin.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

	if timeMax:
		timeMax = dateutil.parser.parse(timeMax)
	else:
		one_week = timedelta(days=7)
		timeMax = timeMin + one_week

	all_future_events_request = service.events().list(
		calendarId = 'primary',
		singleEvents=True,
		timeMin=timeMin.isoformat(),
		timeMax=timeMax.isoformat(),
		orderBy='startTime'
	)
	all_future_events = all_future_events_request.execute()
	future_events = split_events_on_rooms(all_future_events.get('items'))
	future_events = calculate_conflicts(future_events)

	return HttpResponse( json.dumps(future_events),
		content_type="application/json" )

def notify_about_conflicts(request):
	credentials = get_credentials()
	service = services.calendar(credentials)

	timeMin = timezone.now()
	timeMin = timeMin.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

	one_month = timedelta(days=30) # We look one month forward
	timeMax = timeMin + one_month

	all_future_events_request = service.events().list(
		calendarId = 'primary',
		singleEvents=True,
		timeMin=timeMin.isoformat(),
		timeMax=timeMax.isoformat(),
		orderBy='startTime'
	)
	all_future_events = all_future_events_request.execute()
	future_events = split_events_on_rooms(all_future_events.get('items'))
	future_events = calculate_conflicts(future_events)
	declined_events = list()

	for room in future_events:
		for event in room.get('events'):
			declines_event = has_declined_event(event)
			if event.get('conflicts') and not declines_event:
				send_conflict_mail(event, room)
				decline_conflicting_event(event, room)
				declined_events.append(event)

	return HttpResponse( json.dumps( {'declined_events': declined_events} ),
		content_type="application/json" )