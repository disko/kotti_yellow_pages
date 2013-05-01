###*
 * kotti_yellow_pages AngularJS application
 * @type {angular.module}
###
app = angular.module("kotti_yellow_pages", [])

###*
 * mapquest service
 * @return {object}
###
app.factory "mapquest", ($log, $http) ->

  mapquest =

    ###*
     * tile layer for use in Leaflet maps
     * @type {L.tileLayer}
    ###
    tileLayer: L.tileLayer(
      "http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.jpeg",
      attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      subdomains: "1234")

    ###*
     * MapQuest API key
     * @type {String}
    ###
    key: "Fmjtd%7Cluub2q0znd%2Cas%3Do5-9u7sda"

    ###*
     * Return a geolocation for the given address
     * @param  {object} address Object with street, zipcode, city and country
     *                          properties, each of which is of type String.
     * @return {promise}        The callback of the promise object has to
     *                          expect a single argument that can be either
     *                          {false} if no geolocation was found for the
     *                          given address properties or a {L.LatLng}
     *                          object containing the geolocation.
    ###
    latLngForAddress: (address) ->

      $log.info("Requesting geolocation from MapQuest API endpoint...")

      base_url = "http://open.mapquestapi.com/geocoding/v1/address?key=#{mapquest.key}"
      street = if address.street then "#{address.street}" else ""
      zipcode = if address.zipcode then "#{address.zipcode}" else ""
      city = if address.city then "#{address.city}" else ""
      country = if address.country then "#{address.country}" else ""
      address = "#{street}, #{zipcode} #{city}, #{country}"
      $log.info("Constructed addresss: #{address}")
      params =
        inFormat: "kvp"
        outFormat: "json"
        callback: "JSON_CALLBACK"
        location: address

      $log.info(params)

      promise = $http.jsonp(base_url, {params:params})

        .then (response) ->

          $log.info("Received response from MapQuest API endpoint...")

          if response.status != 200
            $log.error("ERROR (status=#{response.status})")

          return response.data.results

      return promise


###*
 * map service
 * @param  {service} mapquest A service providing a tileLayer and
 *                            latLngForAddress method.
 * @param  {service} $http    AngularJS http service
 * @return {L.map}            A map configured with a tileLayer that
 *                            also provides a latLngForAddress method.
###
app.factory "map", ($log, mapquest) ->

  $('#map').height($(window).height() - 40)
  map = L.map("map", zoomControl: true)
  map.latLngForAddress = mapquest.latLngForAddress
  mapquest.tileLayer.addTo(map)

  return map

###*
 * controlGroup directive
 * @return {factory} directive factory
###
app.directive 'controlGroup', () ->
  controlGroup =
    controller: () ->
      #controller cn func, may access $scope, $element, $attrs, $transclude
    restrict: 'A'
    scope:
      controlGroup: "@"
      title: "@"
      required: "@"
      ngModel: "="
    template: """
      <label class="control-label" for="{{controlGroup}}">
        <span>{{title}}</span>
        <span class="req" ng-show="required">*</span>
      </label>
      <div class="controls">
        <span ng-transclude></span>
        <span class="help-inline">{{$parent.errors[controlGroup]}}</span>
      </div>
    """
    replace: false
    transclude: true
    #called IFF compile not defined
    link: (scope, elem, attrs) ->
      elem.addClass('control-group')
      if scope.$parent.errors
        if scope.$parent.errors[attrs.controlGroup]
          elem.addClass('error')

  return controlGroup
