let map, marker, geocoder;

function initMap() {
    geocoder = new google.maps.Geocoder();
    map = new google.maps.Map(document.getElementById('mapa'), {
        center: { lat:  28.1283, lng: -15.4469 }, // Centro inicial en el IES
        zoom: 12
    });

    marker = new google.maps.Marker({
        map: map,
        draggable: true
    });

    document.getElementById('direccion').addEventListener('blur', function() {
        let address = this.value;
        geocodeAddress(address);
    });

    marker.addListener('dragend', function() {
        let position = marker.getPosition();
        document.getElementById('latitud').value = position.lat();
        document.getElementById('longitud').value = position.lng();
    });
}

function geocodeAddress(address) {
    let direccionInput = document.getElementById('direccion');
    let errorText = document.getElementById('error-direccion');

    if (!errorText) {
        // Si el mensaje no existe, lo creamos
        errorText = document.createElement("p");
        errorText.id = "error-direccion";
        errorText.style.color = "red";
        errorText.textContent = "Introduzca una localización correcta";
        errorText.style.display = "none"; // Inicialmente oculto
        direccionInput.insertAdjacentElement("afterend", errorText);
    }

    geocoder.geocode({ address: address }, function(results, status) {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            marker.setPosition(results[0].geometry.location);
            document.getElementById('latitud').value = results[0].geometry.location.lat();
            document.getElementById('longitud').value = results[0].geometry.location.lng();
            // Ocultar mensaje de error si la dirección es válida
            errorText.style.display = "none";  
        } else {
            // Mostrar mensaje de error si la geocodificación falla
            errorText.style.display = "block";
        }
    });
}
