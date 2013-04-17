
$(function () {

    var map, mapquest, marker, position;

    function initMap () {
        map = L.map('map', {zoomControl: true}).setView([51, 10], 6);
        mapquest = L.tileLayer(
            "http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.jpeg",
            {
                attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; ' +
                             'Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                subdomains: '1234'
            }
        ).addTo(map);
        position = new L.LatLng(51, 10);
        marker = L.marker(position, {draggable: true}).addTo(map);
        marker.on('dragend', function(e) {
            $("input[name=latitude]").val(e.target._latlng.lat);
            $("input[name=longitude]").val(e.target._latlng.lng);
        });
    }

    function setLatLng(pos) {
        position.lat = pos.coords.latitude;
        position.lng = pos.coords.longitude;
        $("input[name=latitude]").val(position.lat);
        $("input[name=longitude]").val(position.lng);
        map.setView(position, 14);
        marker.setLatLng(position);
    }

    initMap();

    if (! ($("input[name=latitude]").val() && $("input[name=longitude]").val())) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(setLatLng);
        }
    } else {
        var pos = {
            coords: {
                latitude: $("input[name=latitude]").val(),
                longitude: $("input[name=longitude]").val()
        }};
        setLatLng(pos);
    }

});
