
app = angular.module("kotti_yellow_pages", [])

app.factory "mapquest", () ->

  mapquest =
    tileLayer: L.tileLayer(
      "http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.jpeg",
      attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      subdomains: "1234")
    key: "Fmjtd%7Cluub2q0znd%2Cas%3Do5-9u7sda"

app.factory "addressService", ($http, mapquest) ->

  service = {}

  service.latLngForAddress = (location) ->

    base_url = "http://open.mapquestapi.com/geocoding/v1/address?key=#{mapquest.key}"
    street = if location.street then "#{location.street}" else ""
    zipcode = if location.zipcode then "#{location.zipcode}" else ""
    city = if location.city then "#{location.city}" else ""
    country = if location.country then "#{location.country}" else ""
    location = "#{street}, #{zipcode} #{city}, #{country}"
    params =
      inFormat: "kvp"
      outFormat: "json"
      callback: "JSON_CALLBACK"
      location: location

    console.log params

    promise = $http.jsonp(base_url, {params:params})
      .then (response) ->
        if response.status != 200
          console.log "ERROR"
        console.log "response", response
        results = response.data.results
        if results.length != 1
          console.log "response.data contains #{results.length} results."
          return false
        locations = results[0].locations
        if locations.length != 1
          console.log "results[0] contains #{locations.length} locations."
          return false
        latlng = locations[0].latLng
        latlng = new L.LatLng(latlng.lat, latlng.lng)
        console.log "returning", latlng
        return latlng

    return promise


  return service
