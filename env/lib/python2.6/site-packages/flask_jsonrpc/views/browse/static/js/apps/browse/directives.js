(function(App) {
	'use strict';

	angular.module('browse.directive', [])
        .directive('__prettyprint-it', function() {
            return {
                restrict: 'C',
                link: function postLink(scope, element, attrs) {
                    return element.html(prettyPrintOne('{}'));
                }
            };
        });
	
})(window.App);