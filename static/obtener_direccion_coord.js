window.obtenerDireccion = function(lat, lng, elementId) {
    let geocoder = new google.maps.Geocoder();
    let latlng = new google.maps.LatLng(lat, lng);

    geocoder.geocode({ location: latlng }, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                document.getElementById(elementId).textContent = results[0].formatted_address;
            } else {
                document.getElementById(elementId).textContent = "Ubicación no encontrada";
            }
        } else {
            document.getElementById(elementId).textContent = "Error obteniendo ubicación";
        }
    });
};

document.addEventListener("DOMContentLoaded", function() {
    avistamientos.forEach((avist, index) => {
        let elementId = `lugar-${index}`;
        obtenerDireccion(avist.latitud, avist.longitud, elementId);
    });
});
