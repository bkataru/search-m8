var app = angular.module("searchm8", ["ngRoute"]); 

app.config(function($routeProvider) { // Making the Router Provider
    $routeProvider
        .when("/", {
            templateUrl: "../static/pages/home.html",
            controller: "homeController"
        })
        .when("/result", {
            templateUrl: "../static/pages/result.html",
            controller: "resultController"
        });
});

app.controller('homeController', function($scope, $location, moduleService, dataService) {
    $scope.search = function() {
        var text = $scope.searchResult;
        moduleService.search(text)
            .then(function(results) {
                console.log(results);
                dataService.set(results);
                $location.path('/result');
            })
            .catch(function(err) {
                Materialize.toast('<p class="flow-text red-text">' + err.data.message + '</p>', 2000);
            });
    }
});

app.controller('resultController', function($scope, moduleService, dataService) {
    $scope.resultData = dataService.get();
    console.log(resultData);
})