PagesCtrl = ($scope, $http, $window, $log, $q, map) ->

  ###*
   * Initialize the company objects.
  ###
  initCompanies = ->

    $log.info "initCompanies"

    for company in $scope.companies

      # make company.branches an array of actual branch objects
      _branch_names = (b.title for b in company.branches when b.selected is true)
      company.branches = (b for b in $scope.branches when b.title in _branch_names)

      # also append the company to the branche's companies array
      for branch in company.branches
        branch.companies.push(company)

      # create a marker object on the company if it contains the required
      # (non empty) lat / lng attributes
      if not company.marker and company.location.lat and company.location.lng
        company.latlng = new L.LatLng(company.location.lat, company.location.lng)
        company.marker = new L.marker(company.latlng)

      ###*
       * Determine if the company shoul be visible in the application's current
       * state.
       * @return {bool} true: visible, false: invisible
      ###
      company.visible = ->
        # Determine if any of the company's branches is visible.
        anyBranchVisible = true in (b.visible for b in @branches)

        # Determine if the company's marker is within the current bounds of the
        # map.
        inMapBounds = @latlng and $scope.map.getBounds().contains(@latlng)

        # Return true if all of the above conditions are met.
        return anyBranchVisible and inMapBounds

      company.distanceToMapCenter = ->
        if not @latlng
          return null
        return Math.round(@latlng.distanceTo(map.getCenter()) / 1000, 10)

  ###*
   * Initialize the branch obejcts.
  ###
  initBranches = ->
    $log.info "initBranches"

    # Put a bounds object on each branch that can contain all of its companies.
    for branch in $scope.branches
      branch.bounds = new L.LatLngBounds((c.latlng for c in branch.companies when c.latlng))

  ###*
   * Initialize the map.
  ###
  initMap = ->
    $log.info "initMap"
    $window.map = $scope.map = map

    # Fit the map to a new bounds object that can contain all branches' bounds.
    map.bounds = new L.LatLngBounds((b.bounds for b in $scope.branches))
    map.fitBounds(map.bounds)

    # Add a handler for all relevant map events.
    map.on 'moveend dragend zoomend', (e) ->
      $log.info(e)
      $scope.$apply ->
        $scope.map.getBounds()


  branchesInitialized = $q.defer()
  ###*
   * Wait for the branches object to appear on the scope, then resolve the
   * branchesInitialized promise.
  ###
  $scope.$watch 'branches', (branches) ->
    $log.info "Got #{branches.length} branches."
    $window.branches = branches
    branchesInitialized.resolve()

  companiesInitialized = $q.defer()
  ###*
   * Wait for the companies object to appear on the scope, then resolve the
   * companiesInitialized promise.
  ###
  $scope.$watch 'companies', (companies) ->
    $log.info "Got #{companies.length} companies."
    $window.companies = companies
    companiesInitialized.resolve()

  ###*
   * Wait for the branchesInitialized and companiesInitialized promises to be
   * resolved, then initialize the application.
  ###
  $q.all([branchesInitialized.promise, companiesInitialized.promise]).then ->

    $log.info "Initializing..."

    initCompanies()
    initBranches()
    initMap()

    $scope.updateFilter()

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
