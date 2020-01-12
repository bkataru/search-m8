var app = angular.module("searchm8", ["ngRoute", 'ngYoutubeEmbed']); 

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
}).config(function($sceProvider) {
       $sceProvider.enabled(false);
   });

app.controller('homeController', function($scope, $location, moduleService, dataService) {
    $scope.loading = false;
    $scope.sentence_count_video = 10;
    $scope.sentence_count_article = 10;
    $scope.no_article = 10;
    $scope.no_video = 5;
    $scope.search = function() {
        var text = $scope.searchResult;
        var video_count = $scope.sentence_count_video;
        var text_count = $scope.sentence_count_article;
        var no_article = $scope.no_article;
        var no_video = $scope.no_video;
        if(video_count == 0 || text_count == 0 || no_article == 0 || no_video == 0)
        {
              M.toast({html: '<p class="flow-text red-text">Error: One of video sentence count, text sentence count, max videos, or max articles is 0 </p>'});      
        }
        else
        {
             $scope.loading = true;
             moduleService.search(text, video_count, text_count, no_article, no_video)
            .then(function(results) {
                $scope.loading = false;
                results.text = text;
                console.log(results);
                dataService.set(results);
                M.toast({html: '<p class="flow-text green-text">Your results are ready!</p>'});
                $location.path('/result');
            })
            .catch(function(err) {
                 M.toast({html: '<p class="flow-text red-text">' + err.data.message + '</p>'});
            });   
        }
    }
});

app.controller('resultController', function($scope, $sce, moduleService, dataService) {
    $scope.resultData = dataService.get();
    $scope.videoUrlArr = [];
    for(let elem of $scope.resultData.video_data) {
        $scope.videoUrlArr.push($sce.trustAsResourceUrl('https://youtube.com' + elem.link));
    }    
    console.log($scope.videoUrlArr);
    
    $scope.openTextModal = function(key) {
         var elem = document.getElementById('expanded_summary_text_modal');
         var instance = M.Modal.getInstance(elem);
         $scope.text_modal_desc = $scope.resultData.text_data[key].summary;
         instance.open();
    }
    
    $scope.openVideoModal = function(index) {
        console.log('iajsdiosajd');
        var elem = document.getElementById('expanded_summary_video_modal');
        var instance = M.Modal.getInstance(elem);
        $scope.video_modal_desc = $scope.resultData.video_data[index].summary;
        instance.open();
    }
})