# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from datetime import timedelta, datetime, time
import dateutil.parser
import pytz

import json
from oauth2client import client
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.django_orm import Storage
import re

from aabenthus_com.google import services
from aabenthus_com.google.models import Authorization

from .models import Room

# Used to create iCal feeds for each of the rooms.
from icalendar import Calendar, Event, vCalAddress

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
					event1_created = dateutil.parser.parse( event1.get('updated') )
					event2_created = dateutil.parser.parse( event2.get('updated') )
					if event1_created > event2_created:
						event1['conflicts'] = True
						event1['conflicts_with'] = event2
					else:
						event2['conflicts'] = True
						event2['conflicts_with'] = event1
	return rooms

def add_organizers_images(rooms_and_events):
	#organizer_image
	return rooms_and_events

def send_conflict_mail(event, room):
	organizers_email = event.get('organizer').get('email')

	template_data = {
		'event': event,
		'room': room,
		'rooms_email': settings.ROOMS_EMAIL,
		'frontend_calendar_link': settings.FRONTEND_BASE_URL + '/#/rooms'
	}

	text_content = render_to_string('email-conflicting-event.txt', template_data)
	html_content = render_to_string('email-conflicting-event.html', template_data)

	msg = EmailMultiAlternatives(settings.CONFLICT_MAIL_SUBJECT % event.get('summary'),
		text_content, settings.CONFLICT_MAIL_FROM, [organizers_email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

def change_response_status(event, status):
	credentials = get_credentials()
	service = services.calendar(credentials)

	if event.get('attendees'):
		for attendee in event.get('attendees'):
			if attendee.get('self'):
				attendee['responseStatus'] = status
	else: # Althrough this is very unlikely ..
		event['attendees'] = [{
			'email': settings.ROOMS_EMAIL,
			'responseStatus': status
		}]

	service.events().update(
		calendarId='primary',
		eventId=event['id'],
		body=event
	).execute()

def has_declined_event(event):
	if event.get('attendees'):
		for attendee in event.get('attendees'):
			if attendee.get('self'):
				if attendee['responseStatus'] == 'declined':
					return True
	return False

def get_future_events(timeMin = None, timeMax = None):
	credentials = get_credentials()
	service = services.calendar(credentials)

	if not timeMin:
		timeMin = timezone.now()
		timeMin = timeMin.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

	if not timeMax:
		one_month = timedelta(days=30)
		timeMax = timeMin + one_month

	all_future_events_request = service.events().list(
		calendarId = 'primary',
		singleEvents=True,
		timeMin=timeMin.isoformat(),
		timeMax=timeMax.isoformat(),
		orderBy='startTime'
	)
	all_future_events = all_future_events_request.execute()
	timeZone = pytz.timezone(all_future_events.get('timeZone'))

	morning = time(0, 0, 0, tzinfo = timeZone)
	evening = time(0, 0, 0, tzinfo = timeZone)

	events = all_future_events.get('items')
	for event in events:
		start_dateTime = event.get('start').get('dateTime')
		start_date = event.get('start').get('date')
		end_dateTime = event.get('end').get('dateTime')
		end_date = event.get('end').get('date')

		if start_date:
			start_date = dateutil.parser.parse(start_date)
		if end_date:
			end_date = dateutil.parser.parse(end_date)

		if not start_dateTime and start_date:
			start_dateTime = datetime.combine(start_date, morning)
			event.get('start')['dateTime'] = start_dateTime.isoformat()
		if not end_dateTime and end_date:
			end_dateTime = datetime.combine(end_date, evening)
			event.get('end')['dateTime'] = end_dateTime.isoformat()

	return ( events, timeZone )

# Accessable views

def list_rooms(request):
	rooms = list()
	for room in Room.objects.all():
		room_dict = room.as_dict()
		room_dict['url'] = reverse('booking_ical_feed', kwargs={ 'room_slug': room.slug() })
		room_dict['url'] = request.build_absolute_uri(room_dict['url'])
		rooms.append( room_dict )
	return HttpResponse( json.dumps({
		'rooms': rooms,
		'email': settings.ROOMS_EMAIL
	}), content_type="application/json" )

def list_bookings(request, timeMin = None, timeMax = None):
	timeMin = dateutil.parser.parse(timeMin) if timeMin else None
	timeMax = dateutil.parser.parse(timeMax) if timeMax else None
	all_future_events, timeZone = get_future_events(timeMin, timeMax)
	future_events = split_events_on_rooms(all_future_events)
	future_events = calculate_conflicts(future_events)
	future_events = add_organizers_images(future_events)

	return HttpResponse( json.dumps(future_events),
		content_type="application/json" )

def notify_about_conflicts(request):
	all_future_events, timeZone = get_future_events()
	future_events = split_events_on_rooms(all_future_events)
	future_events = calculate_conflicts(future_events)
	declined_events = list()
	accepted_events = list()

	# Let's first accept all events which needs acceptance.
	# We need to do this before declining to keep the order in which the events
	# have been updated.
	for room in future_events:
		for event in room.get('events'):
			declines_event = has_declined_event(event)
			if not event.get('conflicts') and declines_event:
				change_response_status(event, 'accepted')
				accepted_events.append(event)

	# Then let's decline events which needs to be declined.
	for room in future_events:
		for event in room.get('events'):
			declines_event = has_declined_event(event)
			if event.get('conflicts') and not declines_event:
				send_conflict_mail(event, room)
				change_response_status(event, 'declined')
				declined_events.append(event)

	return HttpResponse( json.dumps( {
		'declined_events': declined_events,
		'accepted_events': accepted_events
	} ), content_type="application/json" )

def booking_ical_feed(request, room_slug):
	rooms = [r for r in Room.objects.all() if r.slug() == room_slug]
	if len(rooms) == 1:
		room = rooms[0]
		# Create a calendar
		cal = Calendar()
		cal['summary'] = u'☑ %s room' % room.title

		all_future_events, timeZone = get_future_events()
		future_events = split_events_on_rooms(all_future_events)
		future_events = calculate_conflicts(future_events)

		for some_room in future_events:
			if some_room.get('title') == room.title:
				for event in some_room.get('events'):
					if not event.get('conflicts'):
						ical_event = Event()

						ical_event.add('id', event.get('iCalUID'))

						start = dateutil.parser.parse( event.get('start').get('dateTime') )
						end = dateutil.parser.parse( event.get('end').get('dateTime') )
						start = start.replace(tzinfo=timeZone)
						end = end.replace(tzinfo=timeZone)
						ical_event.add('dtstart', start)
						ical_event.add('dtend', end)
							
						ical_organizer = vCalAddress( 'MAILTO:%s' % event.get('organizer').get('email') )
						ical_organizer.params['cn'] = event.get('organizer').get('displayName')
						ical_event.add('organizer', ical_organizer)

						if event.get('visibility') == 'private':
							ical_event.add('summary', 'Booked')
						else:
							ical_event.add('summary', event.get('summary'))
							ical_event.add('location', event.get('location'))
							if event.get('attendees'):
								for attendee in event.get('attendees'):
									ical_attendee = vCalAddress('MAILTO:%s' % attendee.get('email'))
									ical_attendee.params['cn'] = attendee.get('displayName')
									ical_event.add('attendee', ical_attendee)

						cal.add_component(ical_event)

		return HttpResponse( cal.to_ical(), content_type="text/calendar" )
	else:
		slugs = ', '.join([room.slug() for room in Room.objects.all()])
		return HttpResponse('Please choose one of the following room slugs: %s' % slugs)