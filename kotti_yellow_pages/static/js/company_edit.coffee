###*
 * CompanyEdit view controller
 * @param {ng.Scope} $scope Controller scope
 * @param {ng.$http} $http  AngularJS HTTP service
 * @param {L.map}    map    Map object with tileLayer and additional
 *                          latLngForAddress method.
###

Function::property = (prop, desc) ->
  Object.defineProperty @prototype, prop, desc

class Address
  complete: false
  constructor: (@_street='', @_zipcode='', @_city='', @_country='') ->
  @property 'street',
    get: -> @_street
    set: (@_street) ->
      @updateComplete()
  @property 'zipcode',
    get: -> @_zipcode
    set: (@_zipcode) ->
      @updateComplete()
  @property 'city',
    get: -> @_city
    set: (@_city) ->
      @updateComplete()
  @property 'country',
    get: -> @_country
    set: (@_country) ->
      @updateComplete()

  updateComplete: ->
    if @_street and @_zipcode and @_city and @_country
      @complete = true
    else
      @complete = false

CompanyEditCtrl = ($scope, $http, $log, map) ->

  # default location
  $scope.location = new L.LatLng(0, 0)

  # bind the map to the scope
  $scope.map = map
  $scope.map.setView($scope.location, 6)

  # create a single marker
  $scope.marker = L.marker($scope.location, draggable: true ).addTo($scope.map)

  ###*
   * Pass the address from the scope to the latLngForAddress service method and
   * update location if a geolocation is returned by the API endpoint.
  ###
  $scope.locateAddress = ->

    $log.info("Updating location from scope.address...")

    if not $scope.addressSubform.$valid
      return false

    # call the addressService
    map.latLngForAddress($scope.company.address).then (latLng) ->
      if latLng
        $scope.company.location.lat = latLng.lat
        $scope.company.location.lng = latLng.lng
        $scope.setMarkerFromLocation()

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

    false

  # Handle the marker's dragend event.
  $scope.marker.on "dragend", (e) ->
    $scope.$apply ->
      $scope.company.location.lat = e.target._latlng.lat
      $scope.company.location.lng = e.target._latlng.lng

  $scope.$watch 'addressSubform.$valid', ->
    # debugger

  handleLocationChange = ->
    l = $scope.company.location
    if not (l and l.lat and l. lng)
      return false
    if not L.LatLng.isPrototypeOf($scope.company.location)
      $scope.company.location = new L.LatLng(l.lat, l.lng)

  $scope.$watch 'company.location.lat', handleLocationChange, false
  $scope.$watch 'company.location.lng', handleLocationChange, false
