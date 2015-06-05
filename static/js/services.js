'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('aips.services', []).
    value('version', '0.1').
    service('CsrfService', ['$cookies' ,function($cookies){
        return {
            'val': function() {
                return $cookies.csrftoken;
            },
            'set_csrf': function(data) {
                data['csrfmiddlewaretoken'] = $cookies.csrftoken;
            },
            'set_csrf_array': function(data){
                data.push({'csrfmiddlewaretoken': $cookies.csrftoken});
            },
            'format_error': function(error) {
                if(error.code == 1){
                    error.type = 'success';
                }else{
                    error.type = 'danger';
                }
                error.show = true;
                return error;
            }
        };
    }]).
    service('UserService', ['urls', '$http', '$cookies', function(urls, $http, $cookies){
        var user = {};
        $.get(urls.api + '/user/status', function(data){
            user = data;
        });
        if($cookies.username){
            user.username = $cookies.username;
        }
        if($cookies.status){
            user.status = $cookies.status;
        }
        if($cookies.role){
            user.role = $cookies.role;
        }
        return {
            'username': function(){
                return user.username;
            },
            'refresh': function(){
                $.get(urls.api + '/user/status', function(data){
                    user = data;
                });
            },
            'status': function(){
                return user.status;
            },
            'role': function(){
                if(!('role' in user)){
                    return 1;
                }
                return user.role;
            },
            'roles': function(){ //What's this?
                return user.roles;
            },
            'school_manager': function(){
                if(!('role' in user)){
                    return false;
                }
                return parseInt(user.role) == 0 || parseInt(user.role) == 4;
            },
            'department_manager': function(){
                if(!('role' in user)){
                    return false;
                }
                return parseInt(user.role) == 0 || parseInt(user.role) == 3;
            },
            'logout': function(){
                $http.get(urls.api + '/user/logout').success(function(data){
                    delete $cookies['username'];
                    delete $cookies['role'];
                    delete $cookies['status'];
                    console.log(data);
                    if(data.error.code == 1){
                        window.location.href = '/';
                    }
                });
            }
        };
    }]).
    filter('cut', function(){
        return function (value, wordwise, max, tail) {
            if (!value) return '';

            max = parseInt(max, 10);
            if (!max) return value;
            if (value.length <= max) return value;

            value = value.substr(0, max);
            if (wordwise) {
                var lastspace = value.lastIndexOf(' ');
                if (lastspace != -1) {
                    value = value.substr(0, lastspace);
                }
            }

            return value + (tail || ' …');
        };
    }).
    filter('uri', function(){
        return function(value) {
            return encodeURIComponent(value);
        };
    }).
    filter('id2date', function(){
        return function(value) {
            var secs = parseInt(value.substring(0,8), 16)*1000;
            var tmp_date = new Date(secs);
            return tmp_date.getFullYear() + '年' + (tmp_date.getMonth() + 1) + '月' + tmp_date.getDate() + '日';
        };
    });
