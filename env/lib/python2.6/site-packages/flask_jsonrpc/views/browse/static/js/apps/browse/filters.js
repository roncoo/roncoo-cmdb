(function(App) {
	'use strict';

	angular.module('browse.filter', [])
        .filter('prettyprint', ['$sanitize', function($sanitize) {
            return function(input) {
                return $sanitize(prettyPrintOne(input));
            };
        }]);
	
})(window.App);
