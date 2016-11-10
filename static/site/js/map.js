
var map = (function() {

    var map = function() {

        var map = L.map(
            'mapid',
            {
                center: [37.8, 0],
                minZoom: 2,
                maxZoom: 18,
                maxBounds: [
                    [-200, -200],
                    [200, 200]
                ],
                attributionControl: false
            }
        ).setView([15, 0], 2);

        (function() {
            var tile1 = L.tileLayer(
                'https://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=edc03de9e53e477bad25250c1116fa36', 
                {
                    attribution: 'Maps &copy <a href="http://www.thunderforest.com">Thunderforest</a>, Data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                }
            );

            tile1.addTo(map);

            L.control.attribution(
            {
                position: 'topright'
            }
            ).addTo(map);

        })();

        return map;

    }();

    $('.nav-pills a[href="#map-result"]').on("shown.bs.tab", function() {
            map.invalidateSize();
    });

    return map;

})();


mapCoordinates = function(map, coordinates) {
    for (i = 0; i < coordinates.length; i++) {
        var coordinate = [coordinates[i][0], coordinates[i][1]];
        var predator = coordinates[i][2];
        var prey = coordinates[i][3];
        var popup = "<table class='table'><tr><td class='field-label'>Predator</td><td>"+predator+"</td></tr><tr><td class='field-label'>Prey</td><td>"+prey+"</td></tr></table>"
        var circle = L.circleMarker(coordinate, {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: 5,
            weight: 1
        }).bindPopup(popup).addTo(map);
    }
}
