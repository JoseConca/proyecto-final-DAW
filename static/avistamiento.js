document.addEventListener('DOMContentLoaded', () => {
    const tipoSelect = document.getElementById('tipo');
    const colorSelect = document.getElementById('color');
    const nombreSelect = document.getElementById('nombre');

    tipoSelect.addEventListener('change', async () => {
        const tipo = tipoSelect.value;
        colorSelect.innerHTML = '<option value="">Seleccionar color</option>';
        nombreSelect.innerHTML = '<option value="">Seleccionar nombre</option>';
        nombreSelect.disabled = true;

        if (tipo) {
            const response = await fetch(`/api/colores?tipo=${tipo}`);
            const data = await response.json();
            colorSelect.disabled = false;
            data.colores.forEach(color => {
                const option = document.createElement('option');
                option.value = color;
                option.textContent = color;
                colorSelect.appendChild(option);
            });
        } else {
            colorSelect.disabled = true;
        }
    });

    colorSelect.addEventListener('change', async () => {
        const tipo = tipoSelect.value;
        const color = colorSelect.value;
        nombreSelect.innerHTML = '<option value="">Seleccionar nombre</option>';
    
        if (tipo && color) {
            const response = await fetch(`/api/mascotas?tipo=${tipo}&color=${color}`);
            const data = await response.json();
            nombreSelect.disabled = false;
            data.mascotas.forEach(mascota => {
                const option = document.createElement('option');
                option.value = mascota.id;  // Aquí usamos el ID de la mascota
                option.textContent = mascota.nombre;
                nombreSelect.appendChild(option);
            });
        } else {
            nombreSelect.disabled = true;
        }
    });
});
