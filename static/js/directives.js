'use strict';

/* Directives */


angular.module('aips.directives', []).
    directive('appVersion', ['version', function(version) {
        return function(scope, elm, attrs) {
            elm.text(version);
        };
    }]).
    directive('userNav', ['urls', '$location', function(urls, $location){
        return {
            restrict: 'E',
            scope: {
                page: '=page'
            },
            controller: function($scope){
                $scope.pages_tab = {
                    'userinfo': {
                        'text': '个人信息管理',
                        'active': false,
                        'url': '/user/maintain_info'
                    },
                    'item': {
                        'text': '基地、计划、项目、导师管理',
                        'active': false,
                        'url': '/item/create'
                    },
                    'message': {
                        'text': '站内消息',
                        'active': false,
                        'url': '/user/message'
                    },
                    'ability': {
                        'text': '个人能力点',
                        'active': false,
                        'url': '/user/point'
                    }
                };
                $scope.pages_tab[$scope.page].active = true;
                $scope.url = function(url){
                    $location.url(url);
                };
            },
            templateUrl: urls.part + '/manager_nav.html'
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
    }]);
