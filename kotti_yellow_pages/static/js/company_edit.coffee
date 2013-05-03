###*
 * CompanyEdit view controller
 * @param {ng.Scope} $scope Controller scope
 * @param {ng.$http} $http  AngularJS HTTP service
 * @param {L.map}    map    Map object with tileLayer and additional
 *                          latLngForAddress method.
###

CompanyEditCtrl = ($scope, $http, $log, map) ->

  # setup the spinner
  $('.spinner').spin({})

  # default location
  $scope.location = new L.LatLng(0, 0)

  # bind the map to the scope
  $scope.map = map
  $scope.map.setView($scope.location, 6)

  # create a single marker
  $scope.marker = L.marker($scope.location, draggable: true ).addTo($scope.map)

  $scope.search =
    status: 'notAllowed' # allowed, inProgress, noResult, singleResult, multipleResults

  $scope.browserSupportsGeolocation = navigator.geolocation

  $scope.invokeNavigatorGeoLocation = ->
    if navigator.geolocation
      navigator.geolocation.getCurrentPosition (position) ->
        $scope.company.location.lat = position.coords.latitude
        $scope.company.location.lng = position.coords.longitude
        $scope.setMarkerFromLocation()

  $scope.selectSearchResult = (location) ->
    latlng = location.latLng
    latlng = new L.LatLng(latlng.lat, latlng.lng)

    $scope.company.location.lat = latlng.lat
    $scope.company.location.lng = latlng.lng
    $scope.setMarkerFromLocation()

    $scope.search.status = 'singleResult'

  ###*
   * Pass the address from the scope to the latLngForAddress service method and
   * update location if a geolocation is returned by the API endpoint.
  ###
  $scope.locateAddress = ->

    if not $scope.addressSubform.$valid
      return false

    $log.info("Updating location from scope.address...")
    $scope.search.results = []
    $scope.search.status = 'inProgress'
    $scope.communicationSubform.$setPristine()

    # call the addressService
    map.latLngForAddress($scope.company.address).then (results) ->

      $scope.searchInProgress = false

      if results.length != 1
        $log.warn("response.data contains #{results.length} results.")
        $scope.search.status = 'noResult'
        return false

      locations = results[0].locations

      switch locations.length
        when 0
          $log.warn("results[0] contains #{locations.length} locations.")
          $scope.search.status = 'noResult'
          # TODO:   call the address service again without the street part of
          #         the address (maybe even without a housenumber (or its
          #         appendix (a/b/c)) first).
          return false
        when 1
          $scope.search.status = 'singleResult'
          $scope.selectSearchResult(locations[0])
          return true
        else
          $scope.search.status = 'multipleResults'
          $scope.search.results = locations
          return false

    return false

  ###*
   * Update the marker position with the location from the scope.  Also update
   * the corresponding input fields' values.
  ###
  $scope.setMarkerFromLocation = ->

    $log.info("Updating marker position and form field values from scope.location...")

    $scope.marker.setLatLng $scope.company.location
    $scope.map.panTo $scope.company.location
    $scope.map.setZoom 14

    true

  # Handle the marker's dragend event.
  $scope.marker.on "dragend", (e) ->
    $scope.$apply ->
      $scope.company.location.lat = e.target._latlng.lat
      $scope.company.location.lng = e.target._latlng.lng

  handleLocationChange = ->
    $log.info("handleLocationChange")
    l = $scope.company.location
    if not (l and l.lat and l. lng)
      return false
    if not L.LatLng.isPrototypeOf($scope.company.location)
      $scope.company.location = new L.LatLng(l.lat, l.lng)
    $scope.setMarkerFromLocation()

  $scope.$watch 'company.location.lat', handleLocationChange, false
  $scope.$watch 'company.location.lng', handleLocationChange, false
