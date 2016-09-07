(function(App) {
    'use strict';

    angular.module('core.service', [])
        .value('PendingRequests', {
            counter: 0,
            increment: function() { 
                this.counter += 1;
            },
            decrement: function() {
                if (this.isPending()) {
                    this.counter -= 1;
                } 
            },
            isPending: function() {
                return this.counter > 0;
            }
        })
        .config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
            cfpLoadingBarProvider.includeSpinner = true;
        }])
        .config(['$httpProvider', 'PendingRequestsProvider', function($httpProvider, PendingRequestsProvider) {
            var PendingRequests = PendingRequestsProvider.$get();
            $httpProvider.responseInterceptors.push("PendingRequestsHttpInterceptor");
            $httpProvider.defaults.transformRequest.push(function(data, headersGetter) {
                PendingRequests.increment();
                return data;
            });
        }])
        .factory('PendingRequestsHttpInterceptor', ['$injector', '$q', '$window', 'PendingRequests', function($injector, $q, $window, PendingRequests) {
            return function(promise) {
                var $http = $injector.get('$http');
                return promise.then(
                    function(response) { // onSuccess
                        PendingRequests.decrement();
                        return response;
                    }, 
                    function(response) { // onError
                        PendingRequests.decrement();
                        return $q.reject(response);
                    }
                );
            };
        }])
        .factory('Storage', function() {
            var localStorage = !!window.localStorage ? window.localStorage : App.localStorage;
            return {
                get: function(key) {
                    return !!localStorage && (key in localStorage) ? localStorage[key] : undefined;
                },
                put: function(key, value) {
                    if (!localStorage) { localStorage = {}; }
                    localStorage[key] = value;
                },
                remove: function(key) {
                    !!localStorage && key in localStorage ? delete localStorage[key] : undefined;
                },
                clear: function() {
                    localStorage = undefined;
                }
            };
        })
        .value('HandlebarsTemplateCache', [])
        .factory('Handlebars', ['HandlebarsTemplateCache', function(HandlebarsTemplateCache) {
            return {
                template: function(templateName, context) {
                    if (!!HandlebarsTemplateCache[templateName]) {
                        return HandlebarsTemplateCache[templateName](context);
                    }

                    var source = $('#' + templateName).html();
                    HandlebarsTemplateCache[templateName] = Handlebars.compile(source);
                    return HandlebarsTemplateCache[templateName](context);
                }
            };
        }]);
        
})(window.App);