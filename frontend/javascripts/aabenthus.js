// declare a module
var module = angular.module('aabenthus', ['ui.router']);

// configure the module.
// in this example we will create a greeting filter
module.config(['$stateProvider', '$urlRouterProvider',
	function($stateProvider, $urlRouterProvider) {
	$urlRouterProvider.otherwise("/rooms");

	$stateProvider
		.state('rooms', {
			url: '/rooms',
			controller: 'roomsCtrl',
			controllerAs: 'rooms',
			templateUrl: '/templates/partials/rooms.html'
		});
}]);