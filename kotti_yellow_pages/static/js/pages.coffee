tiles = L.tileLayer(
  "http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.jpeg",
  attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  subdomains: "1234"
)

PagesCtrl = ($scope, $http) ->

  map = undefined
  mapquest = undefined
  bounds = undefined
  southWest = undefined
  northEast = undefined

  $http.get(window.context_url + "json").success (data) ->

    $scope.companies = data.companies
    $scope.branches = data.branches

    center = new L.LatLng(
      (data.min_lat + data.max_lat) / 2.0,
      (data.min_lng + data.max_lng) / 2.0)

    bounds = new L.LatLngBounds(
      new L.LatLng(data.min_lat, data.min_lng),
      new L.LatLng(data.max_lat, data.max_lng))

    map = L.map("map",
      zoomControl: true
    ).setView(center).fitBounds(bounds)

    mapquest = tiles.addTo(map)

    i = $scope.companies.length - 1

    while i >= 0
      c = $scope.companies[i]
      L.marker(new L.LatLng(c.latitude, c.longitude),
        title: c.title
        riseOnHover: true
      ).addTo(map).bindPopup("<h3>" + c.title + "</h3><p>" + c.street + "</p>").on "click", (e) ->
        @openPopup()

      i--

  $scope.$watch "confirmed", (newValue, oldValue) ->
