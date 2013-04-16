
$(function () {

    var map, mapquest, marker, position;

    map = L.map('map', {zoomControl: true}).setView([latitude, longitude], 8);
    mapquest = L.tileLayer(
        "http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.jpeg",
        {
            attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; ' +
                         'Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            subdomains: '1234'
        }
    ).addTo(map);
    position = new L.LatLng(latitude, longitude);
    marker = L.marker(position, {draggable: false}).addTo(map);

});
