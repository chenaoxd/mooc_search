'use strict';

/* Directives */


angular.module('aips.directives', []).
    directive('appVersion', ['version', function(version) {
        return function(scope, elm, attrs) {
            elm.text(version);
        };
    }]).
    directive('errorMessage', ['urls', function(urls){
        return {
            restrict: 'E',
            scope: {
                error: '=error'
            },
            controller: function($scope){
//                console.log($scope.error);
            },
            templateUrl: urls.part + '/error_message.html'
        };
    }]).directive('selectOnClick', function () {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                element.on('click', function () {
                    if (!window.getSelection().toString()) {
                        // Required for mobile Safari
                        this.setSelectionRange(0, this.value.length);
                    }
                });
            }
        };
    });
