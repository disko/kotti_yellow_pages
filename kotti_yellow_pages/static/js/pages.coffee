# tile layer for the map
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

  $scope.updateFilter = ->
    debugger

  $http.get(window.context_url + "json").success (data) ->

    # center for the map
    center = new L.LatLng(
      (data.min_lat + data.max_lat) / 2.0,
      (data.min_lng + data.max_lng) / 2.0)

    # bounds for the map
    bounds = new L.LatLngBounds(
      new L.LatLng(data.min_lat, data.min_lng),
      new L.LatLng(data.max_lat, data.max_lng))

    # create the map
    map = L.map("map",
      zoomControl: true
    ).setView(center).fitBounds(bounds)

    mapquest = tiles.addTo(map)

    # process the branches
    $scope.branches = {}
    for b in data.branches
      l = new L.LayerGroup()
      l.visible = true
      $scope.branches[b.title] = l
      l.addTo(map)


    $scope.companies = []
    for c in data.companies
      c.visible = true
      m = new L.Marker(new L.LatLng(c.latitude, c.longitude))
      for b in c.branches
        m.addTo($scope.branches[b])
      $scope.companies.push(m)


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
