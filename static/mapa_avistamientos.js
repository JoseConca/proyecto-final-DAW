document.addEventListener('DOMContentLoaded', () => {
    let map = new google.maps.Map(document.getElementById("mapa"), {
        center: { lat: 40.4168, lng: -3.7038 }, // Centro inicial en Madrid
        zoom: 12
    });

    if (avistamientos.length > 0) {
        let bounds = new google.maps.LatLngBounds();

        avistamientos.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));


        avistamientos.forEach((avist, index) => {
            let position = new google.maps.LatLng(parseFloat(avist.latitud), parseFloat(avist.longitud));

            // Calcular tamaño y opacidad en función del índice
            let maxSize = 150; // Tamaño máximo del marcador
            let minSize = 20; // Tamaño mínimo del marcador
            let size = maxSize - ((index / avistamientos.length) * (maxSize - minSize));

            let opacity = 1 - (index / avistamientos.length) * 0.9; // El último será 50% transparente

            let marker = new google.maps.Marker({
                position: position,
                map: map,
                title: `${index + 1}º - ${avist.descripcion}`,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: size / 10, 
                    fillColor: "red",
                    fillOpacity: opacity,
                    strokeWeight: 1,
                    strokeColor: "black"
                }
            });
            //  Obtener la dirección con Geocoder y mostrarla en el infoWindow
            let geocoder = new google.maps.Geocoder();
            geocoder.geocode({ location: position }, function (results, status) {
                let direccion = "Ubicación desconocida";
                if (status === google.maps.GeocoderStatus.OK && results[0]) {
                    direccion = results[0].formatted_address;
                }

                        let infoWindow = new google.maps.InfoWindow({
                            content: `
                                <div style="font-size: 14px;">
                                    <strong>${index + 1}º - ${avist.fecha}</strong><br>
                                    <strong>Lugar:</strong> ${direccion}<br>
                                    <strong>Descripción:</strong> ${avist.descripcion}
                                </div>
                            `
                        });

                        marker.addListener("click", () => {
                            infoWindow.open(map, marker);
                        });
            });

            bounds.extend(position);
        });

            map.fitBounds(bounds);
    }
});

