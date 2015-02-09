var module = angular.module('aabenthus');

module.factory('rooms', ['$http', '$q', function($http, $q) {

	var BASE_URL = 'http://local.api.åbenthus.com';

	this.get_rooms = function() {
		var deferred = $q.defer();
		var url = [BASE_URL, 'rooms'];

		$http.get(url.join('/') + '/').then(function(response) {
			deferred.resolve(response.data);
		}, deferred.reject);

		return deferred.promise;
	};

	this.get_bookings = function(start, end) {
		var deferred = $q.defer();
		var url = [BASE_URL, 'rooms', 'bookings'];

		if(start) {
			url.push( start.toJSON() );
		}
		if(start && end) {
			url.push( end.toJSON() );
		}
		console.log(url);

		$http.get(url.join('/') + '/').then(function(response) {
			deferred.resolve(response.data);
		}, deferred.reject);

		return deferred.promise;
	};

	return this;
}]);