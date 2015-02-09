from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aabenthus_com.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(
    	r'^/?$',
    	'aabenthus_com.rooms.views.list_rooms',
    	name='list_rooms'
    ),
    url(
    	r'^bookings/?$',
    	'aabenthus_com.rooms.views.list_bookings',
    	name='list_bookings'
    ),
    url(
    	r'^bookings/(?P<timeMin>[\d\-T:Z.]+)/(?P<timeMax>[\d\-T:Z.]+)/?$',
    	'aabenthus_com.rooms.views.list_bookings',
    	name='list_bookings_limited'
    ),
    url(
    	r'^bookings/notify-about-conflicts/?$',
    	'aabenthus_com.rooms.views.notify_about_conflicts',
    	name='notify_about_conflicts'
    ),
    url(
    	r'^(?P<room_slug>[a-z]+)/bookings/ical/?$',
    	'aabenthus_com.rooms.views.booking_ical_feed',
    	name='booking_ical_feed'
    )
)
