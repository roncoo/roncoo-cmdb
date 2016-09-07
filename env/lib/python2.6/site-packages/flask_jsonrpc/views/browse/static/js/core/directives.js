(function(App) {
	'use strict';

	angular.module('core.directive', [])
        .directive('disableable', ['$parse', function($parse) {
            return {
                restrict: 'C',
                require: '?ngClick',
                link: function (scope, elem, attrs, ngClick) {
                    elem.bind('click', function (e) {
                        e.stopImmediatePropagation();
                        return false;
                    });

                 }
             };
        }]);
	
})(window.App);