'use strict';


// Declare app level module which depends on filters, and services
angular.module('aips', [
    'ngRoute',
    'ui.tinymce',
    'ui.bootstrap',
    'ngCookies',
    'angularFileUpload',
    'angular-google-analytics',
    'aips.filters',
    'aips.services',
    'aips.directives',
    'aips.controllers',
    //semantic directives
    'angularify.semantic.accordion',
	'angularify.semantic.checkbox',
	'angularify.semantic.dimmer',
	'angularify.semantic.dropdown',
	'angularify.semantic.modal',
	'angularify.semantic.popup',
	'angularify.semantic.rating',
	'angularify.semantic.sidebar',
	'angularify.semantic.wizard'
]).
    constant('urls', {'part': '/static/partials', 'api': '/api'}).
    config(['$interpolateProvider', function($interpolateProvider){
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    }]).
    config(['$httpProvider', function($httpProvider){
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    }]).
    config(['$routeProvider', '$locationProvider', 'urls', function($routeProvider, $locationProvider, urls) {
        //Route configure
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix = '';
        $routeProvider.when('/', {templateUrl: urls.part + '/homepage.html', controller: 'HomepageCtrl', title: 'Homepage'});
        $routeProvider.when('/act/:act_id/manage', {templateUrl: urls.part + '/act_manage.html', controller: 'ActivityManageCtrl', title: "ActivityManage"});
        $routeProvider.when('/dev', {templateUrl: urls.part + '/dev.html', controller: 'DevCtrl', title: 'Dev page'});

        $routeProvider.otherwise({redirectTo: '/'});
    }]).
//  apply a acount number for the detection~
    config(function(AnalyticsProvider){
        AnalyticsProvider.setAccount('UA-60524165-1');
        AnalyticsProvider.trackPages(true);
        AnalyticsProvider.trackUrlParams(true);
        AnalyticsProvider.useDisplayFeatures(true);
    }).
    run(['$location', '$rootScope', function($location, $rootScope){
        //Configure header title of the page
        $rootScope.$on('$routeChangeSuccess', function(event, current, previous){
            $rootScope.title = current.$$route.title;
        });
    }]);
