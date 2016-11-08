
var initializeMap = (function() {

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
                attributionControl: false,
            }, 
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

    $(function() {
        $("body").on("shown.bs.tab", "#map-tab", function() {
                map.invalidateSize();
        });
    });

})();

