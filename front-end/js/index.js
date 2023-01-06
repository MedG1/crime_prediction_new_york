//déclaration des couches openlayers
var lyr_osm = new ol.layer.Tile({
    title: 'OSM',
    type: 'base',
    visible: true,
    source: new ol.source.OSM()
});

var layersList = [lyr_osm];

var mapView = new ol.View({
    projection: 'EPSG:3857',
    center: new ol.geom.Point([-8239393.9994, 40.7090]).transform('EPSG:4326', 'EPSG:3857').getCoordinates(),
    zoom: 7
});

var map = new ol.Map({
    target: 'map',
    layers: layersList,
    view: mapView
});
var MousePosition = new ol.control.MousePosition({
    coordinateFormat: ol.coordinate.createStringXY(4),
    projection: 'EPSG:4326'
});
map.addControl(MousePosition)

map.on('pointermove', function (event) {
    var coord3857 = event.coordinate;
    var coord4326 = ol.proj.transform(coord3857, 'EPSG:3857', 'EPSG:4326');
    $('#mouse3857').text(ol.coordinate.toStringXY(coord3857, 2));
    $('#mouse4326').text(ol.coordinate.toStringXY(coord4326, 5));
});
var location_array = []
map.on('singleclick', function (evt) {
    onSingleClick(evt);
});
var onSingleClick = function (evt) {
    var coord = evt.coordinate;
    console.log(coord);
    location_array = coord
    document.getElementById('lon').value = location_array[0]
    document.getElementById('lat').value = location_array[1]
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Geolocation

function prediction() {
    gender_elements = document.getElementsByName("Gender")
    for (i = 0; i < gender_elements.length; i++) {
        if (gender_elements[i].checked) {
            gender = gender_elements[i].value;
        }
    }
    race_elements = document.getElementsByName("Race")
    for (i = 0; i < race_elements.length; i++) {
        if (race_elements[i].checked) {
            race = race_elements[i].value;
        }
    }
    age = document.getElementById("age").value
    date = document.getElementById("date").value
    console.log(document.getElementById("date").valueAsDate)
    hour = document.getElementById("hour").value
    place_elements = document.getElementsByName("Place")
    for (i = 0; i < place_elements.length; i++) {
        if (place_elements[i].checked) {
            place = place_elements[i].value;
        }
    }
    if (location_array.length == 0) {
        alert("Please indicate your position")
    }
    else {
        //new lines

        ////
        result = fetch('http://localhost:8080/prediction', {
            method: 'POST',
            body: JSON.stringify({
                gender: gender,
                race: race,
                age: age,
                day: 12,
                month: 10,
                year: 2016,
                hour: hour,
                place: place,
                lat: location_array[0],
                lon: location_array[1]
            }),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        })

        // result.then(response => {
        //     console.log(response)
        //     return response.body;
        // }).then(pred => {
        //     console.log(pred);
        //     document.getElementById("resulttt").value = pred;
        // })
        result.then(response => response.json())
            .then(data => { 
                document.getElementById("resulttt").value = data["result"];
                console.log(data); 
            })
    }
}
