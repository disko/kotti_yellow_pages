###*
 * Controller for the Yellow Pages main view.
###
PagesCtrl = ($scope, $http, $window, $log, $q, map) ->

  ###*
   * safeApply - see: https://coderwall.com/p/ngisma
  ###
  $scope.safeApply = (fn) ->
    phase = this.$root.$$phase
    if(phase == '$apply' or phase == '$digest')
      if (fn and (typeof(fn) == 'function'))
        fn()
    else
      this.$apply(fn)

  ###*
   * Initialize the company objects.
  ###
  initCompanies = ->

    for company in $scope.companies

      # make company.branches an array of actual branch objects
      _branch_names = (b.title for b in company.branches when b.selected is true)
      company.branches = (b for b in $scope.branches when b.title in _branch_names)

      # also append the company to the branche's companies array
      for branch in company.branches
        branch.companies.push(company)

      ###*
       * Get or set wether the company details should be visible.
       * @param  {bool} show         if given: set the visible state, else: get
       * @param  {bool} recurse=true if true and show is also true: set all other
       *                             compnies' detail visible state to false.
       * @return {bool}              the visible state
      ###
      company.showDetails = (show, recurse=true) ->
        if show in [true, false]
          @_showDetails = show
          if @marker
            if show
              @marker.setIcon(@marker.selectedIcon)
            else
              @marker.setIcon(@marker.defaultIcon)
        if show and recurse
          for c in $scope.companies
            if c != @
              c.showDetails(false, false)
        return @_showDetails

      ###*
       * Handler for the company's marker's click result.
       * @param  {L.MouseEvent} e The event that triggered the handler
      ###
      company.onClick = (e) ->
        $log.info "click"
        $scope.safeApply ->
          e.target.setIcon(e.target.selectedIcon)
          e.target.company.showDetails(true)

      # create a marker object on the company if it contains the required
      # (non empty) lat / lng attributes
      if not company.marker and company.location.lat and company.location.lng

        company.latlng = new L.LatLng(company.location.lat, company.location.lng)

        marker = new L.marker(company.latlng, title:company.title, riseOnHover:true, riseOffset: 1000)
        marker.company = company

        marker.defaultIcon = map.makeIcon(color:'darkblue', icon:'question-sign')
        marker.hoverIcon = map.makeIcon(color:'blue', icon:'info-sign')
        marker.selectedIcon = map.makeIcon(color:'red', icon:'star')
        marker.setIcon(marker.defaultIcon)

        marker.on "click", company.onClick

        marker.on "mouseover", (e) ->
          marker = e.target
          if marker.options.icon not in [marker.selectedIcon, marker.hoverIcon]
            marker.setIcon(marker.hoverIcon)

        marker.on "mouseout", (e) ->
          marker = e.target
          if marker.options.icon not in [marker.selectedIcon, marker.defaultIcon]
            marker.setIcon(marker.defaultIcon)

        company.marker = marker

      ###*
       * Determine if the company shoul be visible in the application's current
       * state.
       * @return {bool} true: visible, false: invisible
      ###
      company.visible = ->
        # Determine if any of the company's branches is visible.
        anyBranchVisible = true in (b.visible for b in @branches)

        # Determine if the company's marker is within the current
        # bounds of the map.
        inMapBounds = @latlng and $scope.map.getBounds().contains(@latlng)

        # Return true if all of the above conditions are met.
        return anyBranchVisible and inMapBounds

      ###*
       * Determine the distance to the current center of the map.
       * @return {int} Distance in km
      ###
      company.distanceToMapCenter = ->
        if not (@latlng and $scope.mapCenter)
          return @distance = null
        return @distance = Math.round(@latlng.distanceTo($scope.mapCenter) / 1000, 10)

      ###*
       * Determine the distance to the location provided by the user.
       * @return {int} Distance in km
      ###
      company.distanceToUser = ->
        if not (@latlng and $scope.user.latlng)
          return @distance = null
        return @distance = Math.round(@latlng.distanceTo($scope.user.latlng) / 1000, 10)

  $scope.distanceToMapCenter = (company) ->
    if company.distanceToMapCenter
      return company.distanceToMapCenter()
    else
      return false

  $scope.distanceToZipcode = (company) ->
    if company.distanceToUser
      return company.distanceToUser()
    else
      return false

  $scope.companyName = (company) ->
    return company.title

  $scope.companyZipcode = (company) ->
    return company.zipcode

  $scope.companyListOrder = (company) ->
    if not $scope.listOrderBy
      $scope.listOrderBy = 'companyZipcode'
    return $scope[$scope.listOrderBy](company)

  $scope.recalcDistances = ->
    (c.distanceToMapCenter() for c in companies when c.distanceToMapCenter)

  $scope.numCompaniesVisible = ->
    return (c for c in companies when c.visible()).length

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

    # Add a handler for all relevant map events.
    map.on 'load moveend dragend zoomend', (e) ->
      $scope.safeApply ->
        $scope.map.getBounds()
        $scope.mapCenter = $scope.map.getCenter()
        $scope.recalcDistances()

    # Fit the map to a new bounds object that can contain all branches' bounds.
    map.bounds = new L.LatLngBounds((b.bounds for b in $scope.branches))
    map.fitBounds(map.bounds)

  $scope.updateBranchesVisible = ->
    $log.info "updateBranchesVisible"
    for branch in $scope.branches
      for company in branch.companies
        if company.marker
          if branch.visible and not map.hasLayer(company.marker)
            map.addLayer(company.marker)
          if not branch.visible and map.hasLayer(company.marker)
              map.removeLayer(company.marker)

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

  $scope.latLngForUser = ->

    # only handles German zipcodes correctly atm
    if not $scope.user or $scope.user.zipcode.length != 5
      $('.companies_listing').slideUp()
      return false

    $('.companies_listing').slideDown()

    map.latLngForAddress($scope.user).then (response) ->
      if response.length > 0
        locations = response[0].locations
        if locations.length > 0
          location = response[0].locations[0]
          latlng = location.latLng
          $scope.user.latlng = new L.LatLng(latlng.lat, latlng.lng)

          # Zoom to level 13 on zipcode change, then zoom out until at least one
          # marker is visible.
          if $scope.listOrderBy = 'distanceToZipcode'
            $scope.safeApply ->
              map.panTo($scope.user.latlng)
              zoomend = (e) ->
                if $scope.numCompaniesVisible() <= 1
                  map.zoomOut()
                else
                  map.off('zoomend', zoomend)
              map.on('zoomend', zoomend)
              map.setZoom(13)

  $scope.$watch 'user', $scope.latLngForUser, true

  ###*
   * Wait for the branchesInitialized and companiesInitialized promises to be
   * resolved, then initialize the application.
  ###
  $q.all([branchesInitialized.promise, companiesInitialized.promise]).then ->

    $log.info "Initializing..."
    initCompanies()
    initBranches()
    initMap()

    $scope.listOrderBy = 'distanceToMapCenter'
    $window.user = $scope.user =
      zipcode: ''
      country: 'DE'

    $scope.latLngForUser()

    $scope.updateBranchesVisible()
