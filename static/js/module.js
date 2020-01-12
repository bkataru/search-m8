var app = angular.module("searchm8");
app.service('moduleService', function($http) {
    var moduleService = [];
    moduleService.search = function(text, video_count, text_count, no_article, no_video) {
        // no_video: number of videos to search through
        // video_count: number of sentences for summary
       return $http({
            method: "GET",
            url: `./searchQuery?query=` + text + '&video_sentence_count=' + video_count + '&text_sentence_count=' + text_count
            + '&no_article=' + no_article + '&no_video=' + no_video,
            headers: { 'Content-Type': 'application/json' },
        }).then(function(responses) {
            console.log(responses.data);
            return responses.data;
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