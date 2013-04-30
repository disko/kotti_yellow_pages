###*
 * Company view controller
 * @param {ng.Scope} $scope Controller scope
 * @param {L.map}    map    Map object with tileLayer and additional
 *                          latLngForAddress method.
###

CompanyCtrl = ($scope, map) ->

  initMap = ->

    $scope.location = new L.LatLng($scope.lat, $scope.lng)
    $scope.map = map
    $scope.map.setView($scope.location, 12)
    $scope.marker = L.marker($scope.location, draggable: false ).addTo($scope.map)

  $scope.$watch 'lat', ->
    if $scope.lng
      initMap()

  $scope.$watch 'lng', ->
    if $scope.lat
      initMap()

