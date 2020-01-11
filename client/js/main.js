var app = angular.module("searchm8", ["ngRoute"]); 

app.config(function($routeProvider) { // Making the Router Provider
    $routeProvider
        .when("/", {
            templateUrl: "../pages/home.html",
            controller: "homeController"
        });
});
app.controller('homeController', function($scope) {
    
});