PagesCtrl = ($scope, $http, $window, $log, map) ->

  $scope.$watch 'branches', (branches) ->
    $log.info "Initializing branches"
    $window.branches = branches
    $window.map = $scope.map = map
    createMapElements()
    $scope.updateFilter()

  createMapElements = ->
    $log.info "createMapElements"

    for branch in $scope.branches
      for company in branch.companies
        if not company.marker and company.location.lat and company.location.lng
          company.latlng = new L.LatLng(company.location.lat, company.location.lng)
          company.marker = new L.marker(company.latlng)
      branch.bounds = new L.LatLngBounds((c.latlng for c in branch.companies when c.latlng))

    map.bounds = new L.LatLngBounds((b.bounds for b in $scope.branches))
    map.fitBounds(map.bounds)

  $scope.updateFilter = ->
    $log.info "updateFilter"
    bounds = []
    for branch in $scope.branches
      if branch.visible
        bounds.push(branch.bounds)
      for company in branch.companies
        if company.marker
          if branch.visible and not map.hasLayer(company.marker)
            map.addLayer(company.marker)
          if not branch.visible and map.hasLayer(company.marker)
              map.removeLayer(company.marker)

    if bounds.length > 0

      map.fitBounds(bounds)

#    debugger

  # $http.get(window.context_url + "json").success (data) ->

  #   # center for the map
  #   center = new L.LatLng(
  #     (data.min_lat + data.max_lat) / 2.0,
  #     (data.min_lng + data.max_lng) / 2.0)

  #   # bounds for the map
  #   bounds = new L.LatLngBounds(
  #     new L.LatLng(data.min_lat, data.min_lng),
  #     new L.LatLng(data.max_lat, data.max_lng))

  #   # create the map
  #   map = L.map("map",
  #     zoomControl: true
  #   ).setView(center).fitBounds(bounds)

  #   mapquest = tiles.addTo(map)

  #   # process the branches
  #   $scope.branches = {}
  #   for b in data.branches
  #     l = new L.LayerGroup()
  #     l.visible = true
  #     $scope.branches[b.title] = l
  #     l.addTo(map)


  #   $scope.companies = []
  #   for c in data.companies
  #     c.visible = true
  #     m = new L.Marker(new L.LatLng(c.latitude, c.longitude))
  #     for b in c.branches
  #       m.addTo($scope.branches[b])
  #     $scope.companies.push(m)


  #   i = $scope.companies.length - 1

  #   while i >= 0
  #     c = $scope.companies[i]
  #     L.marker(new L.LatLng(c.latitude, c.longitude),
  #       title: c.title
  #       riseOnHover: true
  #     ).addTo(map).bindPopup("<h3>" + c.title + "</h3><p>" + c.street + "</p>").on "click", (e) ->
  #       @openPopup()

  #     i--

  # $scope.$watch "confirmed", (newValue, oldValue) ->
