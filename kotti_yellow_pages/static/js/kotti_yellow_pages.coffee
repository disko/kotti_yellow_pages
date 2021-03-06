###*
 * kotti_yellow_pages AngularJS application
 * @type {angular.module}
###
app = angular.module("kotti_yellow_pages", ["ui"])

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

      street = if address.street then "#{address.street}" else ""
      zipcode = if address.zipcode then "#{address.zipcode}" else ""
      city = if address.city then "#{address.city}" else ""
      country = if address.country then "#{address.country}" else ""
      addressString = "#{street}, #{zipcode} #{city}, #{country}"
      $log.info("Constructed addresss: #{address}")

      location =
        city: address.city
        country: address.country
        postalCode: address.zipcode
        street: address.street

      params =
        inFormat: "json"
        outFormat: "json"
        callback: "JSON_CALLBACK"
        # location: addressString
        #json: )

      # key and json are part of the base_url (and not in the params object)
      # because angular urlencodes everything provided in params object which
      # doesn't work with the mapquest API.
      base_url = "http://open.mapquestapi.com/geocoding/v1/address?key=#{mapquest.key}&json=#{angular.toJson({location:location})}"
      $log.info(params)

      promise = $http.jsonp(base_url, {params:params})

        .then (response) ->

          $log.info("Received response from MapQuest API endpoint...")

          if response.status != 200
            $log.error("ERROR (status=#{response.status})")

          $log.info(response.data.results)

          # Some of the results (or the locations therein) are obviously wrong.
          # Discard them and only return those that might match the query.
          results = []
          for r in response.data.results
            pl = r.providedLocation
            locations = []
            for l in r.locations
              if (l.adminArea1 == pl.country) and (l.postalCode == pl.postalCode)
                locations.push(l)
            r.locations = locations
            results.push(r)

          return results

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

  $('#map').height($('#map').width())

  map = L.map("map", zoomControl: true, scrollWheelZoom: false)
  mapquest.tileLayer.addTo(map)

  map.latLngForAddress = mapquest.latLngForAddress

  ###*
   * Create and return a marker icon.
   * @param  {object} opts={} Object with non default icon properties.
   * @return {L.Icon}         Marker icon
  ###
  map.makeIcon = (opts={}) ->

    opts.color ?= 'green'
    opts.icon ?= null
    opts.iconColor ?= 'white'
    opts.spin ?= false

    return new L.AwesomeMarkers.icon(opts)

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
