var app = angular.module("searchm8");
app.service('moduleService', function($http) {
    var moduleService = [];
    moduleService.search = function(text) {
       return $http({
            method: "GET",
            url: `./searchQuery?query=` + text,
            headers: { 'Content-Type': 'application/json' },
        }).then(function(responses) {
            console.log(responses.data.results);
            return responses.data.results;
        });
    };
    
    return moduleService;
});

app.factory('dataService', function() {
     var savedData = {}
     function set(data) {
         savedData = data;
     }
     function get() {
         return savedData;
     }

     return {
         set: set,
         get: get
     }
});