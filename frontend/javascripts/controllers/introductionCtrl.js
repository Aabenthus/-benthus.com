var module = angular.module('aabenthus');

module.controller('introductionCtrl', ['$scope', function($scope) {
	$scope.backgrounds = [
		{ src: '/images/introduction-1.png' },
		{ src: '/images/introduction-2.png' }
	];
	$scope.selected_background = Math.floor( Math.random() * $scope.backgrounds.length );

	$scope.companies = [
		{ logo_src: '/images/airtame-logo.png', link: 'https://airtame.com/' },
		{ logo_src: '/images/socialsquare-logo.png', link: 'http://socialsquare.dk/' }
	];

}]).directive('backImg', function() {
	return function(scope, element, attrs){
		attrs.$observe('backImg', function(value) {
			element.css({
				'background-image': 'url(' + value +')',
				'background-size' : 'cover'
			});
		});
	};
});
