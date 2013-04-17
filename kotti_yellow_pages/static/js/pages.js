function PagesCtrl($scope, $http) {
    $scope.center = { lat: 40.094882122321145, lng: -3.8232421874999996 };
    $scope.marker = { lat: 40.094882122321145, lng: -3.8232421874999996 };
    $scope.message = "Drag me to your node position";
    $scope.zoom = 4;

    $http.get('json').success(function(data) {
        $scope.companies = data.companies;
        $scope.branches = data.branches;
    });
    $scope.$watch('confirmed', function(newValue, oldValue) {});
}

// $(function() {

//     var map, mapquest, marker, position;

//     position = new L.LatLng(0, 0);

//     function setLatLng(pos) {
//         position.lat = pos.coords.latitude;
//         position.lng = pos.coords.longitude;
//         map.setView(position, 6);
//     }

//     map = L.map('map', {zoomControl: true}).setView([position.lat, position.lng], 6);
//     mapquest = L.tileLayer(
//         "http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.jpeg",
//         {
//             attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; ' +
//                          'Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
//             subdomains: '1234'
//         }
//     ).addTo(map);
//     // lg = L.layerGroup().addTo(map);
//     // lc = L.control.layers(
//     //     {"Map Quest": mapquest},
//     //     {"Sprite Markers": lg, "Regular Marker": orig}
//     // ).addTo(map);
//     // marker = L.marker(position, {draggable: false}).addTo(map);

//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(setLatLng);
//     }


// });
