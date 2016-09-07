(function(App) {
    'use strict';

    var breadcrumbs = function(name) {
        if (name.indexOf('.') !== -1) {
            var names = name.split('.');
            return [names[0], name];
        }
        return [name];
    };

    App.controller('ApplicationCtrl', ['$scope', '$location', '$timeout',
                                       'responseExample', 'responseObjectExample', 'PendingRequests', 
                                       function($scope, $location, $timeout,
                                                responseExample, responseObjectExample, PendingRequests) {
        $scope.showFakeIntro = true;
        $scope.showContentLoaded = true;
        $scope.showToolbar = false;
        $scope.breadcrumbs = breadcrumbs('Dashboard');
        $scope.response = responseExample;
        $scope.response_object = responseObjectExample;

        $scope.$on('App:displayFakeIntro', function(event, display) {
            $scope.showFakeIntro = display;
        });

        $scope.$on('App:displayContentLoaded', function(event, display) {
            $scope.showContentLoaded = display;
        });

        $scope.$on('App:breadcrumb', function(event, breadcrumb) {
            $scope.breadcrumbs = breadcrumbs(breadcrumb);
        });

        $scope.$on('App:displayToolbar', function(event, display) {
            $scope.showToolbar = display;
        });

        $scope.showSpinner = function() {
            return PendingRequests.isPending();
        };

        $scope.routeIs = function(route) {
            if (Object.prototype.toString.call(route) === '[object Array]') {
                for (var i = 0; i < route.length; i++) {
                    if ('/'+route[i] === $location.path()) {
                        return true;
                    }
                }
                return false;
            } 
            return ('/'+route === $location.path());
        };
    }]);

    App.controller('MenuCtrl', ['$scope', '$location', '$timeout',
                                'Handlebars', 'Api', 
                                function($scope, $location, $timeout,
                                         Handlebars, Api) {
        $scope.$emit('App:displayFakeIntro', true);
        $scope.$emit('App:displayContentLoaded', true);
        Api.packages(function(packages) {
            $scope.packages = packages;
            $scope.$emit('App:displayFakeIntro', false);
            $timeout(function() {
                $scope.$emit('App:displayContentLoaded', false);
            }, 750);
        });

        $scope.showTooltip = function(module) {
            return Handlebars.template('menu-module-tooltip', module);
        };

        $scope.showReponseObject = function(module) {
            return $location.path(module.name);
        };
    }]);

    App.controller('ViewerContainerCtrl', ['$scope', '$location', function($scope, $location) {
        $scope.resend = function() {
            $scope.$broadcast('RPC:resend');
        };

        $scope.changeParameters = function() {
            $scope.$broadcast('RPC:changeParameters');
        };

        $scope.notify = function() {
            $scope.$broadcast('RPC:notify');
        };
    }]);

    App.controller('ModuleDialogCtrl', ['$scope', '$modalInstance', 'module', function($scope, $modalInstance, module) {
        $scope.module = module;

        $scope.ok = function() {
            $modalInstance.close(module);
        };

        $scope.hitEnter = function(evt) {
            if (angular.equals(evt.keyCode,13) && !(angular.equals($scope.name,null) || angular.equals($scope.name,''))) {
                $scope.ok();
            }
        };

        $scope.cancel = function() {
            $modalInstance.dismiss('cancel');
        };
    }]);

    App.controller('ResponseObjectCtrl', ['$scope', '$window', '$modal', 'RPC', 'module', function($scope, $window, $modal, RPC, module) {
        $scope.module = module;
        //$scope.$emit('App:displayContentLoaded', true);
        $scope.$emit('App:displayToolbar', true);
        $scope.$emit('App:breadcrumb', module.name);

        var RPCCall = function(module) {
            RPC.call(module).success(function(response_object, status, headers, config) { // success
                var headers_pretty = headers();
                headers_pretty.data = config.data;

                $scope.response = {status: status, headers: headers_pretty, config: config};
                $scope.response_object = response_object;
                $scope.$emit('App:displayContentLoaded', false);
            }).error(function(response_object, status, headers, config) { // error
                var headers_pretty = headers();
                headers_pretty.data = config.data;

                $scope.response = {status_code: status, headers: headers_pretty, config: config};
                $scope.response_object = undefined;
                $scope.$emit('App:displayContentLoaded', false);
            });
        },
        RPCCallModal = function(module) {
            $modal.open({
                templateUrl: 'module_dialog.html',
                controller: 'ModuleDialogCtrl',
                resolve: {
                    module: function() {
                        return $scope.module;
                    }
                }
            }).result.then(function(module) { // ok
                return RPCCall(module);
            }, function() { // cancel
                $scope.$emit('App:displayContentLoaded', false);
                $window.history.back();
            });
        };

        $scope.$on('RPC:resend', function(event) {
            return RPCCall($scope.module);
        });
        
        $scope.$on('RPC:changeParameters', function(event) {
            return RPCCallModal($scope.module);
        });

        $scope.$on('RPC:notify', function(event) {
            var m = angular.copy($scope.module);
            m.notify = true;
            return RPCCall(m);
        });

        if (!module.params || !module.params.length) {
            return RPCCall(module);
        }

        return RPCCallModal(module);
    }]);

})(window.App);
