var module = angular.module('aabenthus');

module.controller('roomsCtrl', ['rooms', '$scope', 'rooms_information',
	function(rooms, $scope, rooms_information) {

	$scope.loading = false;
	$scope.information_visible = false;
	$scope.rooms_information = rooms_information;

	var PADDING = 10;
	var REFRESH_RATE = 30*1000; // Every 30 seconds.
	
	$('#calendar').fullCalendar({
		// put your options and callbacks here
		firstDay: 1,
		defaultView: 'agendaWeek',
		firstHour: 8,
		timeFormat: 'H:mm',
		axisFormat: 'H(:mm)',
		minTime: '8:00:00',
		slotEventOverlap: false,
		businessHours: {
			start: '9:00',
			end: '17:00',
			dow: [ 1, 2, 3, 4, 5 ]
		},
		hiddenDays: [ 6, 0 ],
		events: function(start, end, timezone, callback) {
			var events = [];
			rooms.get_bookings(start, end).then(function(rooms) {
				for(var r in rooms) {
					var room = rooms[r];
					//var room_class = room.title.toLowerCase().replace(' ', '-');
					for(var e in room.events) {
						var event = room.events[e];
						var eventClassNames = [event.status];
						if(event.conflicts) {
							eventClassNames.push('conflicts');
						}
						var event_start = event.start.date ? event.start.date : event.start.dateTime;
						var event_end = event.end.date ? event.end.date : event.end.dateTime;
						var event_data = {
							title: event.summary,
							start: event_start,
							end: event_end,
							color: room.color,
							textColor: 'white',
							//className: room_class
							className: eventClassNames.join(' '),
							glyphicon: room.glyphicon,
							organizer_initials: event.organizer.initials
						};
						events.push(event_data);
					}
				}
				callback(events);
			});
		},
		eventRender: function(event, element) {
			if(event.glyphicon) {
				$(element).append('<span class="glyphicon glyphicon-'+event.glyphicon+'">');
				if(event.organizer_initials) {
					$organizer_container = $('<div class="organizer"></div>');
					$organizer_container.css({
						'background-color': $(element).css('background-color')
					});
					$organizer = $('<span></span>');
					$organizer.text(event.organizer_initials);
					$organizer_container.append($organizer);
					//$organizer.css('background-image', 'url(' +event.organizer_photo+ ')');
					$(element).append($organizer_container);
				}
			}
		},
		loading: function(isLoading, view) {
			console.log(isLoading);
			$scope.loading = isLoading;
		}
	});

	$(window).resize(function() {
		$('#calendar').fullCalendar('option', 'height', $(window).height() - PADDING * 2);
	});
	// Let's trigger this once.
	$(window).trigger('resize');
	$('#calendar').on('click', '.fc-widget-content', function() {
		$scope.$apply(function() {
			$scope.information_visible = true;
		});
	});

	setInterval(function() {
		$('#calendar').fullCalendar( 'refetchEvents' );
	}, REFRESH_RATE);
}]);