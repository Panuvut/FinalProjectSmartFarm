
angular.module('myApp', []).controller('myCtrl', function($scope, $http) {
        $scope.name = 'testname'
        $scope.duration = 50
        $scope.high_temperature = 50
        $scope.low_temperature = 0
        $scope.high_moisture = 50
        $scope.low_moisture = 0
        $scope.high_ph = 50
        $scope.low_ph = 0
        $scope.etc = 0
        $scope.test = 't1'

        $scope.myfunction = function(submit){
            $scope.test = 't2'
            	$http.get("/set_update_standard",{ 
                        params:{ a : $scope.name,
                                 b : $scope.duration,
                                 c : $scope.high_temperature,
                                 d : $scope.low_temperature,
                                 e : $scope.high_moisture,
                                 f : $scope.low_moisture,
                                 g : $scope.high_ph,
                                 h : $scope.low_ph,
                                 i : $scope.etc
                                }
                        }
                ).then(function (response) {
            			$scope.status = response.data.status;
            	});
	
         
            }
 
        
    });

