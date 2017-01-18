//bat_plot.js should be loaded for this javascript to work
//
//

  var app = angular.module('myApp', []);
  app.run(function($rootScope){
    $rootScope.dict = {
      "Timestamp" : -1,
      "Current" : -1,
      "MVoltage" : -1,
      "Sl1Voltage" : -1,
      "Sl2Voltage" : -1,
      "Sl3Voltage" : -1,
      "Sl4Voltage" : -1,
      "Sl5Voltage" : -1,
      "Sl6Voltage" : -1,
      "Sl7Voltage" : -1,
      "temp1"      : -1,
      "temp2"      : -1,
      "temp3"      : -1,
      "temp4"      : -1,
      "temp5"      : -1,
      "temp6"      : -1,
      "temp7"      : -1,
      "temp8"      : -1,
      "temp9"      : -1
    };
  });
  
  app.controller('myCtrl', function($scope, $rootScope, $http, $timeout) {
      $scope.stamp2date = function(timestamp){
        var date = new Date(timestamp*1000);
        var hours = date.getHours();
        var minutes = "0" + date.getMinutes();
        var seconds = "0" + date.getSeconds();
        var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
        return formattedTime
      }
      $scope.getData = function(){
          console.log(location.hostname)
          $http.get("http://"+location.hostname+":5000/ActualValues")
          .then(function(response) {
              $rootScope.dict = response.data;
              $rootScope.dict["Current"] = response.data["Current"].toFixed(2);
              $rootScope.dict["Timestamp"] = $scope.stamp2date(response.data["Timestamp"]);
              $rootScope.dict["1"] = response.data["MVoltage"].toFixed(5);
              $rootScope.dict["2"] = response.data["Sl1Voltage"].toFixed(5);
              $rootScope.dict["3"] = response.data["Sl3Voltage"].toFixed(5);
              $rootScope.dict["4"] = response.data["Sl2Voltage"].toFixed(5);
              $rootScope.dict["temp1"] = response.data["temp1"].toFixed(2);
              $rootScope.dict["temp2"] = response.data["temp2"].toFixed(2);
              $rootScope.dict["temp3"] = response.data["temp3"].toFixed(2);
              $rootScope.dict["temp4"] = response.data["temp4"].toFixed(2);
              //$rootScope.dict["Sl4Voltage"] = response.data["Sl4Voltage"].toFixed(5);
              //$rootScope.dict["Sl5Voltage"] = response.data["Sl5Voltage"].toFixed(5);
              //$rootScope.dict["Sl6Voltage"] = response.data["Sl6Voltage"].toFixed(5);
              //$rootScope.dict["Sl7Voltage"] = response.data["Sl7Voltage"].toFixed(5);
          });
      };
      $scope.intervalFunction = function(){
          $timeout(function(){
              $scope.getData();
              $scope.intervalFunction();
          }, 1000)
      };
      $scope.intervalFunction();
  });
  
  app.directive('draw', function($rootScope){
      return {
          restrict: 'A',
          scope: true,
          link: function postLink(scope, element, attrs){
              function test(element){
                  var canvas = newCanvas(element);
                  var bat1 = addBat(canvas);
                  bat1 = scale(bat1, 1.5)
                  var divel = canvas.parent().id;

                  var text = canvas.text("");
                  var tspan1 = text.tspan("")
                  tspan1.clear()
                  tspan1.text(function(add) {
                      add.tspan('-1')
                      add.tspan(function(addMore) {
                          addMore.tspan("-1").newLine()
                      })
                  })
                  text.font({
                    family: 'Computer Modern',
                    anchor: 'middle',
                    size: 16 
                  })
                  centerOnCanvasText(canvas, text)
                  centerOnCanvas(canvas, bat1);
                  //console.log(scope.$root.dict["Sl5Voltage"])
                  scope.$root.$watch('dict["'+divel.toString()+'"]', function(newVal, oldVal){
                    //console.log('dict["'+divel.toString()+'"]')
                    //console.log(newVal)
                    tspan1.clear()
                    //tspan2.clear()
                    tspan1.text(function(add) {
                        add.tspan(newVal.toString()+' V')
                        add.tspan(function(addMore) {
                            addMore.tspan(" ").newLine()
                            addMore.tspan(function(addEvenMore) {
                                addEvenMore.tspan(scope.$root.dict["temp"+divel.toString()] + "°C").newLine()
                            })
                        })
                    })
                    text.build(false)
                    //text.tspan(newVal.toString()+' V').tspan('test')
                  });
              }
            test(element[0]);
            }
          };
  });
  

