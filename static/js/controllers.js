'use strict';

/* Controllers */

angular.module('aips.controllers', []).
    controller('HomepageCtrl', ['$scope', '$http', 'CsrfService', 'urls', '$filter', '$routeParams', 'UserService',  '$anchorScroll', function($scope, $http, $csrf, urls, $filter, $routeParams, $user, $anchorScroll){
        console.log('HomepageCtrl');
        $scope.query = '自然语言处理';
        $scope.search_course = function(){
            var param = {
                query: $scope.query
            };
            $http.get(urls.api + '/search_course?' + $.param(param)).success(function(data){
                console.log(data);
                $scope.course_list = data.courses;
                $anchorScroll(0);
            });
        };
        $scope.search_course();
    }]).
    controller('ActivityManageCtrl', ['$scope', '$http', 'CsrfService', 'urls', '$filter', '$routeParams', 'UserService', function($scope, $http, $csrf, urls, $filter, $routeParams, $user){
        console.log('ActivityManageCtrl');
    }]).
    controller('DevCtrl', ['$scope', '$http', 'urls', 'CsrfService', function($scope, $http, urls, $csrf){
        //console.log('DevCtrl');
        $scope.api_url = '/test';
        $scope.param_list = [];
        $scope.add_param = function(){
            $scope.param_list.push({'key':'', 'value':''});
        };
        $scope.response = {};
        $scope.api_post = function(){
            var param_dict = {};
            for(var index in $scope.param_list){
                param_dict[$scope.param_list[index]['key']] = $scope.param_list[index]['value'];
            }
            //console.log(param_dict);
            $csrf.set_csrf(param_dict);
            $http.post(urls.api + $scope.api_url, $.param(param_dict)).success(function(data){
                //console.log(data);
                $scope.response = data;
            });
        };
        $scope.api_get = function(){
            var param_url = '';
            for(var index in $scope.param_list){
                if(index != 0){
                    param_url += '&';
                }else{
                    param_url = '?';
                }
                param_url += $scope.param_list[index]['key'] + '=' + $scope.param_list[index]['value'];
            }
            //console.log(param_url);
            $http.get(urls.api + $scope.api_url + param_url).success(function(data){
                //console.log(data);
                $scope.response = data;
            });
        };
        $scope.clean_param = function(){
            $scope.param_list = [];
        };
    }]);
