(function() {
    'use-strict';

    angular
        .module('keytools', [
            'ui.router',
            'ui.bootstrap'
        ])
        .config(config);

    config.$inject = ['$stateProvider', '$urlRouterProvider'];
    function config($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: 'partials/_home.html'
            })
            .state('key2pub', {
                url: '/key2pub',
                templateUrl: 'partials/_key2pub.html',
                controller: function($scope, $http) {
                    $scope.extractPubkey = function() {
                        $http({
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            url: 'http://10.1.70.60:4999/key2pub',
                            data: {
                                key: $scope.key,
                                passphrase: $scope.passphrase
                            }
                        })
                        .then(function(resp) {
                            $scope.error = undefined;
                            $scope.publicKey = resp.data.public_key;
                        })
                        .catch(function(resp) {
                            $scope.publicKey = undefined;
                            if (!resp.data) {
                                $scope.error = 'API Offline';
                            } else {
                                $scope.error = resp.data.error;
                            }
                        });
                    };
                }
            })
            .state('csr', {
                url: '/csr',
                templateUrl: 'partials/_csr.html'
            });
    }
})();
