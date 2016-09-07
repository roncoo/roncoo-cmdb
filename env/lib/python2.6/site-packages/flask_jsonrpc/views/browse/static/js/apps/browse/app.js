(function(root) {
	'use strict';

	var App = angular.module('browse', ['ngRoute', 'ngResource', 'ngSanitize', 'ngAnimate', 
        'ui.bootstrap', 'chieffancypants.loadingBar',
		'core.service', 'core.directive', 'core.filter', 
		'browse.service', 'browse.directive', 'browse.filter'
		]).
		config(['$routeProvider', 'urlPrefix', function($routeProvider, urlPrefix) {
	    	$routeProvider
	    		.when('/', {
	    			reloadOnSearch: false,
	    			templateUrl: urlPrefix + '/partials/dashboard.html',
                    controller: 'ApplicationCtrl'
	    		})
                .when('/:method', {
                    controller: 'ResponseObjectCtrl',
                    templateUrl: urlPrefix + '/partials/response_object.html',
                    resolve: {
                        module: ['$route', 'Api', function($route, Api) {
                            return Api.method({service: $route.current.params.method}).$promise;
                        }]
                    }
                })
	    		.otherwise({
	    			redirectTo: urlPrefix
	    		});
		}]);

	App.adjust = function() {
        var viewPortHeight = $(window).outerHeight(true),
            viewPortWidth = $(window).outerWidth(true),
            viewPortMenu = viewPortHeight - $('#navbar-main').outerHeight(true) - $('#logo-section').outerHeight(true) - $('#box-subscribe').outerHeight(true),
            viewPortContent = viewPortHeight - $('#navbar-main').outerHeight(true) - $('#viewer-header-container').outerHeight(true),
            viewPortIframe = viewPortContent - $('#title-and-status-container').outerHeight(true);

        // Menu
    	$('#scrollable-sections').height(viewPortMenu);

        // Content master
    	$('#viewer-entries-container').height(viewPortContent);
    };

	App.ready = function(E) {
		// 
        $(window).bind('load resize scroll', function(env) {
            App.adjust();
        });

        // JSON highlighting
        prettyPrint();
	};

	root.App = App;
})(window);