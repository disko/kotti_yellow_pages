CompanyEditCtrl = ($scope, $http, addressService, mapquest) ->

  updateAddress = (name, value) ->
    $scope.$apply ->
      $scope.address[name] = value

  $scope.location = new L.LatLng(51, 10)
  $scope.address =
    street: $('input[name=street]')
      .change ->
        updateAddress("street", this.value)
      .val()
    zipcode: $('input[name=zipcode]')
      .change ->
        updateAddress("zipcode", this.value)
      .val()
    city: $('input[name=city]')
      .change ->
        updateAddress("city", this.value)
      .val()
    country: $('input[name=country]')
      .change ->
        updateAddress("country", this.value)
      .val()

  $scope.setLocationFromAddress = ->
    addressService.latLngForAddress($scope.address).then (latLng) ->
      if latLng
        $scope.location = latLng
        $scope.setMarkerFromLocation()
    return false

  $scope.setMarkerFromLocation = ->
    $scope.marker.setLatLng $scope.location
    $scope.map.panTo $scope.location
    $scope.map.setZoom 14
    $("input[name=latitude]").val $scope.location.lat
    $("input[name=longitude]").val $scope.location.lng

  initMap = ->
    $scope.map = L.map("map",
      zoomControl: true
    ).setView($scope.location, 6)
    mapquest.tileLayer.addTo($scope.map)
    $scope.marker = L.marker($scope.location,
      draggable: true
    ).addTo($scope.map)
    $scope.marker.on "dragend", (e) ->
      $("input[name=latitude]").val e.target._latlng.lat
      $("input[name=longitude]").val e.target._latlng.lng

  setLatLng = (pos) ->
    $scope.location.lat = pos.coords.latitude
    $scope.location.lng = pos.coords.longitude
    $("input[name=latitude]").val $scope.location.lat
    $("input[name=longitude]").val $scope.location.lng
    $scope.map.setView $scope.location, 14
    $scope.marker.setLatLng $scope.location

  initMap()
  unless $("input[name=latitude]").val() and $("input[name=longitude]").val()
    navigator.geolocation.getCurrentPosition setLatLng if navigator.geolocation
  else
    pos = coords:
      latitude: $("input[name=latitude]").val()
      longitude: $("input[name=longitude]").val()

    setLatLng pos

  $scope.$watch 'address', $scope.setLocationFromAddress, true
  $scope.$watch 'location', $scope.marker.update, true
